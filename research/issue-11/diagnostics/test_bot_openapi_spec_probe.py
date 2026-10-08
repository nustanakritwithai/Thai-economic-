"""Mocked source/parser tests, never contact BOT."""
import json
import unittest
from bot_openapi_spec_probe import download, parse_spec, summarize, HOST, PATH


class Response:
    def __init__(self, raw, status=200):
        self.raw, self.status = raw, status
    def getheader(self, name):
        return "application/octet-stream" if name.lower() == "content-type" else None
    def read(self, limit):
        return self.raw[:limit]


class Conn:
    def __init__(self, response):
        self.res = response
        self.calls = []
    def request(self, method, path, body=None, headers=None):
        self.calls.append((method, path, body, dict(headers or {})))
    def getresponse(self):
        return self.res
    def close(self):
        pass


def factory(conn):
    def open_conn(host, port, timeout, context):
        assert host == HOST and port == 443 and timeout <= 10 and context is not None
        return conn
    return open_conn


def doc(path="/category_list/get", base="https://gateway.api.bot.or.th/categorylist"):
    return json.dumps({"openapi": "3.0.3", "servers": [{"url": base}],
                       "paths": {path: {"get": {"responses": {"200": {}, "401": {}}}}},
                       "components": {"securitySchemes": {
                           "a": {"type": "apiKey", "in": "header", "name": "Authorization",
                                 "x-example": "SECRET_CANARY_DO_NOT_PRINT"}}}}).encode()


class TestSpec(unittest.TestCase):
    def test_valid_get_exact(self):
        conn = Conn(Response(doc()))
        r, raw = download(connection_factory=factory(conn), ctx_factory=object)
        self.assertEqual(r["classification"], "RAW_OFFICIAL_GET_OPERATION_AND_BASE_VERIFIED")
        self.assertEqual(r["metadata"]["exact_candidate_documented_status_keys"], ["200", "401"])
        self.assertEqual(len(conn.calls), 1)
        self.assertEqual(conn.calls[0][0:3], ("GET", PATH, None))
        self.assertNotIn("Authorization", conn.calls[0][3])
        self.assertIsNotNone(raw)
        self.assertNotIn("SECRET_CANARY_DO_NOT_PRINT", json.dumps(r))
    def test_different_path_remains_unknown(self):
        r, raw = download(connection_factory=factory(Conn(Response(doc("/category_list/")))), ctx_factory=object)
        self.assertTrue(r["is_valid_openapi"])
        self.assertFalse(r["candidate_get_method_proven"])
    def test_different_server_remains_unknown(self):
        r, raw = download(connection_factory=factory(Conn(Response(doc(base="https://elsewhere.invalid/x")))), ctx_factory=object)
        self.assertFalse(r["candidate_get_method_proven"])
    def test_unrelated_html_not_spec(self):
        r, raw = download(connection_factory=factory(Conn(Response(b"<html>login</html>"))), ctx_factory=object)
        self.assertFalse(r["is_valid_openapi"])
        self.assertIsNone(raw)
    def test_no_follow_redirect(self):
        conn=Conn(Response(b"",302))
        r, raw = download(connection_factory=factory(conn), ctx_factory=object)
        self.assertEqual(r["http_status"],302)
        self.assertEqual(len(conn.calls),1)
        self.assertIsNone(raw)
    def test_size_cap(self):
        r,raw=download(connection_factory=factory(Conn(Response(b"x"*2_000_001))),ctx_factory=object)
        self.assertEqual(r["classification"],"DOWNLOAD_EXCEEDS_SIZE_CAP")
        self.assertIsNone(raw)
    def test_parse_invalid(self):
        kind,data=parse_spec(b'{"openapi":')
        self.assertIsNone(data)
        self.assertNotEqual(kind,"JSON")
    def test_paths_not_confused_with_auth_fields(self):
        meta=summarize(json.loads(doc()))
        self.assertEqual(meta["security_schemes_authorization_header_only"],
                         [{"type":"apiKey","in":"header","name":"Authorization"}])


if __name__=="__main__":
    unittest.main()
