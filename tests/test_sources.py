"""RED tests for sources.py — URL validation, hash verify, safe zip extract."""
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path


class TestSources(unittest.TestCase):
    def test_validate_url_accepts_http_https(self):
        from src.zenfox_install import sources
        sources.validate_url("https://github.com/a/b.zip")
        sources.validate_url("http://example.com/x.zip")
        with self.assertRaises(sources.SourceError):
            sources.validate_url("file:///etc/passwd")
        with self.assertRaises(sources.SourceError):
            sources.validate_url("javascript:alert(1)")
        with self.assertRaises(sources.SourceError):
            sources.validate_url("https://user:pass@example.com/x.zip")

    def test_verify_sha256(self):
        from src.zenfox_install import sources
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "a.bin"
            f.write_bytes(b"hello")
            good = hashlib.sha256(b"hello").hexdigest()
            self.assertTrue(sources.verify_sha256(f, good))
            with self.assertRaises(sources.SourceError):
                sources.verify_sha256(f, "0" * 64)

    def test_safe_extract_allowlist_and_zipslip(self):
        from src.zenfox_install import sources
        with tempfile.TemporaryDirectory() as d:
            z = Path(d) / "t.zip"
            with zipfile.ZipFile(z, "w") as zf:
                zf.writestr("user.js", "x")
                zf.writestr("../../evil.js", "evil")
                zf.writestr("subdir/nested.js", "n")
            out = Path(d) / "out"
            got = sources.safe_extract(z, out, allowlist={"user.js"})
            self.assertEqual(got, [out / "user.js"])
            self.assertFalse((out / "evil.js").exists())
            self.assertFalse(any(out.rglob("evil.js")))

    def test_download_local_http(self):
        from functools import partial
        from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
        from src.zenfox_install import sources
        import threading
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "f.zip").write_bytes(b"data123")
            handler = partial(SimpleHTTPRequestHandler, directory=d)
            srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
            t = threading.Thread(target=srv.serve_forever, daemon=True)
            t.start()
            try:
                url = f"http://127.0.0.1:{srv.server_port}/f.zip"
                dest = Path(d) / "dl.zip"
                sources.download(url, dest)
                self.assertEqual(dest.read_bytes(), b"data123")
            finally:
                srv.shutdown()


if __name__ == "__main__":
    unittest.main()
