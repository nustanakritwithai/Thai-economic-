"""Offline simulations ONLY; real BOT account and token never used."""
import json
import socket
import unittest
from bot_r3_positive_auth import probe, preconditions, HOST, PATH, APPROVAL_FLAGS


class PoisonEnv:
    def get(self, *args):
        raise AssertionError("No environment read in offline mode")


def env():
    values = {x: "YES" for x in APPROVAL_FLAGS}
    values["BOT_STATISTICS_API_TOKEN"] = "SYNTHETIC_SECRET_NEVER_LOG_123"
    return values


class FakeResponse:
    def __init__(self, status=200, mime="application/json", body=b'{"result":{"category":[{"category":"A"}]}}'):
        self.status, self.mime, self.body = status, mime, body
        self.read_calls = 0
    def getheader(self, name):
        return self.mime if name.lower() == "content-type" else None
    def read(self, n):
        self.read_calls += 1
        return self.body[:n]
    def close(self):
        pass


class FakeConnection:
    def __init__(self, response=None, error=None):
        self.response = response or FakeResponse()
        self.error = error
        self.calls = []
    def request(self, method, path, body=None, headers=None):
        self.calls.append((method, path, body, dict(headers)))
        if self.error:
            raise self.error
    def getresponse(self):
        return self.response
    def close(self):
        pass


def build(c):
    def make(host, port, timeout, context):
        assert host == HOST and port == 443 and timeout == 8 and context is not None
        return c
    return make


class TestR3(unittest.TestCase):
    def test_offline_never_reads_env(self):
        r, token = preconditions(live=False, env=PoisonEnv())
        self.assertIsNone(token)
        self.assertEqual(r["request_count"], 0)
        self.assertEqual(r["status"], "BLOCKED_OFFLINE_PREFLIGHT_NO_REQUEST")

    def test_unapproved_does_not_read_token(self):
        class Guarded:
            def get(self, key):
                if key == "BOT_STATISTICS_API_TOKEN":
                    raise AssertionError("Do not access token before approval")
                return None
        r, token = preconditions(live=True, env=Guarded())
        self.assertIsNone(token)
        self.assertEqual(r["status"], "BLOCKED_APPROVAL_OR_PRIVATE_RUNNER_UNVERIFIED")

    def test_approved_but_no_token_fails_closed(self):
        vals = env()
        del vals["BOT_STATISTICS_API_TOKEN"]
        c = FakeConnection()
        r = probe(live=True, env=vals, factory=build(c), context_factory=object)
        self.assertEqual(r["status"], "BLOCKED_APPROVED_TOKEN_NOT_PROVISIONED_IN_THIS_RUNTIME")
        self.assertEqual(c.calls, [])

    def test_reject_newlines_in_secret(self):
        vals = env()
        vals["BOT_STATISTICS_API_TOKEN"] += "\nheader: bad"
        r = probe(live=True, env=vals, factory=build(FakeConnection()), context_factory=object)
        self.assertEqual(r["status"], "BLOCKED_UNSAFE_SECRET_VALUE")
        self.assertEqual(r["request_count"], 0)

    def test_synthetic_expected_200_still_not_gate_pass(self):
        c = FakeConnection()
        r = probe(live=True, env=env(), factory=build(c), context_factory=object, clock=lambda: 2.0)
        self.assertEqual(r["status"], "HTTP_200_EXPECTED_CATEGORY_JSON_PENDING_HUMAN_REVIEW")
        self.assertEqual(r["http_status"], 200)
        self.assertTrue(r["category_structure_valid"])
        self.assertFalse(r["positive_test_approved"])
        self.assertFalse(r["operational_security_certified"])
        self.assertEqual(r["day02_gate"], "BLOCKED_CRITICAL_EVIDENCE")
        self.assertEqual(len(c.calls), 1)
        method, path, body, headers = c.calls[0]
        self.assertEqual((method, path, body), ("GET", PATH, None))
        self.assertEqual(headers["Authorization"], env()["BOT_STATISTICS_API_TOKEN"])
        self.assertNotIn("SYNTHETIC_SECRET_NEVER_LOG", json.dumps(r))

    def test_401_never_reads_raw_error_body(self):
        resp = FakeResponse(status=401, body=b'{"private":"secret"}')
        c = FakeConnection(response=resp)
        r = probe(live=True, env=env(), factory=build(c), context_factory=object)
        self.assertEqual(r["status"], "HTTP_OBSERVED_NO_POSITIVE_ACCESS_PROOF")
        self.assertEqual(resp.read_calls, 0)
        self.assertNotIn("private", json.dumps(r))

    def test_html_200_does_not_pass(self):
        resp = FakeResponse(mime="text/html")
        r = probe(live=True, env=env(), factory=build(FakeConnection(resp)), context_factory=object)
        self.assertEqual(r["status"], "HTTP_200_UNEXPECTED_MIME_NOT_PASS")
        self.assertEqual(resp.read_calls, 0)

    def test_large_200_does_not_pass(self):
        r = probe(live=True, env=env(), factory=build(FakeConnection(
            FakeResponse(body=b"x" * 262145))), context_factory=object)
        self.assertEqual(r["status"], "HTTP_200_RESPONSE_TOO_LARGE_FOR_RESEARCH")

    def test_synthetic_transport_failure_never_leaks_exception_message(self):
        c = FakeConnection(error=socket.gaierror(-2, "SYNTHETIC_SECRET_NEVER_LOG_123"))
        r = probe(live=True, env=env(), factory=build(c), context_factory=object)
        self.assertEqual(r["status"], "LOCAL_OR_TRANSPORT_FAILURE_NO_POSITIVE_PROOF")
        self.assertIsNone(r["http_status"])
        self.assertNotIn("SYNTHETIC_SECRET_NEVER_LOG", json.dumps(r))

    def test_wrong_shape_not_positive(self):
        r = probe(live=True, env=env(), factory=build(FakeConnection(
            FakeResponse(body=b'{"message":"ok"}'))), context_factory=object)
        self.assertEqual(r["status"], "HTTP_200_UNEXPECTED_RESPONSE_SHAPE_NOT_PASS")
        self.assertFalse(r["category_structure_valid"])


if __name__ == "__main__":
    unittest.main()
