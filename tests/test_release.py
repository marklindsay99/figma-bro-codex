import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_manager", ROOT / "scripts/manage.py")
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)


class ReleaseTests(unittest.TestCase):
    def test_separately_installed_payloads_retain_full_mit_notice(self):
        license_text = (ROOT / "LICENSE").read_text()
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Mark Lindsay", license_text)
        with tempfile.TemporaryDirectory() as temporary:
            installation = manager.Manager(Path(temporary), ROOT)
            installation.install()
            self.assertEqual((installation.targets["skill"] / "LICENSE").read_text(), license_text)
            comment_notice = "".join(("# " + line if line else "#") + "\n" for line in license_text.splitlines())
            self.assertTrue(installation.targets["agent"].read_text().startswith(comment_notice))
            installation.uninstall()


if __name__ == "__main__":
    unittest.main()
