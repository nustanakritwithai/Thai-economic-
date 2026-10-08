"""Offline tests for the BOT no-auth network preflight."""
import socket
import unittest
from bot_network_probe import probe_host, make_summary


class FakeSocket:
    def __init__(self, fail=None):
        self.fail = fail
        self.closed = False

    def settimeout(self, _value):
        pass

    def connect(self, _address):
        if self.fail:
            raise self.fail

    def close(self):
        self.closed = True


class FakeTLSConnection:
    def __enter__(self):
        return self

    def __exit__(self, _typ, _err, _tb):
        return False

    def version(self):
        return "TLSv1.3"


class FakeContext:
    def __init__(self, fail=None):
        self.fail = fail
        self.hostname = None

    def wrap_socket(self, _sock, server_hostname):
        self.hostname = server_hostname
        if self.fail:
            raise self.fail
        return FakeTLSConnection()


def resolve(host, port, type=None):
    assert host.endswith("bot.or.th") and port == 443 and type == socket.SOCK_STREAM
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.12", 443))]


class NetworkTest(unittest.TestCase):
    def test_host_allowlist(self):
        with self.assertRaises(ValueError):
            probe_host("example.com", resolver=resolve)

    def test_dns_error_does_not_invent_http(self):
        def fail(*_a, **_kw):
            raise socket.gaierror(-2, "synthetic")
        x = probe_host("gateway.api.bot.or.th", resolver=fail)
        self.assertEqual(x["result"], "BLOCKED_DNS")
        self.assertEqual(x["http_requests"], 0)
        self.assertIsNone(x["origin_http_status"])

    def test_dns_empty(self):
        x = probe_host("gateway.api.bot.or.th", resolver=lambda *_a, **_kw: [])
        self.assertEqual(x["result"], "BLOCKED_DNS")

    def test_tcp_error_does_not_invent_http(self):
        x = probe_host("gateway.api.bot.or.th", resolver=resolve,
                       socket_factory=lambda *_a: FakeSocket(TimeoutError("synthetic")))
        self.assertEqual(x["result"], "BLOCKED_TCP")
        self.assertIsNone(x["origin_http_status"])

    def test_tls_error_stays_tls(self):
        ctx = FakeContext(OSError("synthetic TLS"))
        x = probe_host("gateway.api.bot.or.th", resolver=resolve,
                       socket_factory=lambda *_a: FakeSocket(),
                       context_factory=lambda: ctx)
        self.assertEqual(x["result"], "BLOCKED_TLS")
        self.assertEqual(x["tcp"], "PASS")
        self.assertIsNone(x["origin_http_status"])

    def test_good_tls_is_not_api_success(self):
        ctx = FakeContext()
        x = probe_host("gateway.api.bot.or.th", resolver=resolve,
                       socket_factory=lambda *_a: FakeSocket(),
                       context_factory=lambda: ctx)
        self.assertEqual(x["result"], "PASS_DNS_TCP_TLS")
        self.assertEqual(ctx.hostname, "gateway.api.bot.or.th")
        self.assertFalse(x["authorization_sent"])
        self.assertEqual(x["http_requests"], 0)
        self.assertIsNone(x["origin_http_status"])
        note = make_summary({"checked_at_utc": "test",
                             "runner": {"workflow_run_id": "test", "commit_sha": "test"},
                             "hosts": [x]})
        self.assertIn("not R3/R4 HTTP", note)


if __name__ == "__main__":
    unittest.main()
