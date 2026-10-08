"""Strictly offline tests. No BOT requests are performed in this suite."""
import socket
import unittest
from bot_http_negative_probe import HOST, PATH, METHOD, probe, sanitize_mime


class Response:
    def __init__(self, status=401, mime="application/json", headers=None):
        self.status = status
        self._mime = mime
        self.headers = dict(headers or {})
        self.body_read = False
        self.closed = False

    def getheader(self, name):
        if name.lower() == "content-type":
            return self._mime
        return next((v for k, v in self.headers.items() if k.lower() == name.lower()), None)

    def read(self, *args):
        self.body_read = True
        raise AssertionError("Raw provider body must never be read")

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, response=None, connection_error=None, response_error=None):
        self.response = response or Response()
        self.connection_error = connection_error
        self.response_error = response_error
        self.requests = []
        self.closed = False

    def request(self, method, path, body=None, headers=None):
        self.requests.append((method, path, body, dict(headers or {})))
        if self.connection_error:
            raise self.connection_error

    def getresponse(self):
        if self.response_error:
            raise self.response_error
        return self.response

    def close(self):
        self.closed = True


def fakefactory(connection):
    def make(host, port, timeout, context):
        assert host == HOST and port == 443 and timeout <= 7 and context is not None
        return connection
    return make


class NoAuthTests(unittest.TestCase):
    def test_single_get_and_status_401_uninterpreted(self):
        resp = Response(status=401, mime="application/json; charset=utf-8",
                        headers={"WWW-Authenticate": "untrusted arbitrary value",
                                 "Set-Cookie": "private"})
        conn = FakeConnection(response=resp)
        r = probe(connection_factory=fakefactory(conn),
                  context_factory=object, monotonic=lambda: 1,
                  utc_now=lambda: "2026-10-09T00:00:00Z")
        self.assertEqual(r["response_http_status"], 401)
        self.assertTrue(r["response_observed"])
        self.assertFalse(r["bot_origin_error_semantics_verified"])
        self.assertEqual(r["classification"], "HTTP_RESPONSE_AT_BOT_GATEWAY_HOST_STATUS_UNINTERPRETED")
        self.assertEqual(r["request_count"], 1)
        self.assertEqual(len(conn.requests), 1)
        method, path, body, headers = conn.requests[0]
        self.assertEqual((method, path), ("GET", "/categorylist/category_list/get"))
        self.assertIsNone(body)
        self.assertEqual(set(headers), {"Accept", "User-Agent", "Connection"})
        self.assertFalse(resp.body_read)
        self.assertTrue(conn.closed)
        self.assertNotIn("Cookie", str(r))
        self.assertNotIn("private", str(r))

    def test_200_does_not_claim_auth_success(self):
        conn = FakeConnection(response=Response(status=200, mime="text/html"))
        r = probe(connection_factory=fakefactory(conn), context_factory=object)
        self.assertEqual(r["response_http_status"], 200)
        self.assertFalse(r["bot_authentication_contract_pass"])

    def test_302_does_not_follow_redirect(self):
        conn = FakeConnection(response=Response(status=302, headers={"Location": "https://anywhere.example/secret"}))
        r = probe(connection_factory=fakefactory(conn), context_factory=object)
        self.assertEqual(r["response_http_status"], 302)
        self.assertTrue(r["response_header_presence"]["location"])
        self.assertFalse(r["followed_redirect"])
        self.assertEqual(len(conn.requests), 1)
        self.assertNotIn("anywhere.example", str(r))

    def test_dns_failure_is_not_http_error(self):
        conn = FakeConnection(connection_error=socket.gaierror(-2, "synthetic DNS"))
        r = probe(connection_factory=fakefactory(conn), context_factory=object)
        self.assertIsNone(r["response_http_status"])
        self.assertFalse(r["response_observed"])
        self.assertEqual(r["failure_layer"], "DNS")
        self.assertEqual(r["request_count"], 1)

    def test_http_parse_failure_is_not_origin_status(self):
        conn = FakeConnection(response_error=ValueError("synthetic"))
        r = probe(connection_factory=fakefactory(conn), context_factory=object)
        self.assertEqual(r["failure_layer"], "LOCAL_CLIENT")
        self.assertIsNone(r["response_http_status"])

    def test_mime_allowlist_sanitizes_header(self):
        self.assertEqual(sanitize_mime("Application/JSON; charset=utf-8"), "application/json")
        self.assertEqual(sanitize_mime("text/html; charset=UTF-8"), "text/html")
        self.assertEqual(sanitize_mime("http://example.com/path"), "UNPARSEABLE_NOT_RETAINED")
        self.assertIsNone(sanitize_mime(None))


if __name__ == "__main__":
    unittest.main()
