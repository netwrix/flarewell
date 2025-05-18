import os
import re
import shutil
from pathlib import Path
import subprocess
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = REPO_ROOT / "tests" / "input_docs"
SITE_DIR = REPO_ROOT / "tests" / "test_website"
DOCS_DIR = SITE_DIR / "docs"


def run_cmd(cmd, cwd=None):
    subprocess.check_call(cmd, cwd=cwd or REPO_ROOT)


def setUpModule():
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    run_cmd(
        [
            "python",
            "-m",
            "flarewell.cli",
            "convert",
            "--input-dir",
            str(INPUT_DIR),
            "--output-dir",
            str(DOCS_DIR),
        ]
    )
    run_cmd(["npm", "run", "build"], cwd=SITE_DIR)


def _has_unescaped_braces(text):
    in_code = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not in_code and re.search(r"(?<!\\)[{}]", line):
            return True
    return False


class ConversionTests(unittest.TestCase):
    def test_secure_no_unescaped_braces(self):
        content = Path(DOCS_DIR / "Secure.md").read_text()
        self.assertFalse(_has_unescaped_braces(content))

    def test_performance_no_unescaped_braces(self):
        content = Path(DOCS_DIR / "PerformanceMonitoring.md").read_text()
        self.assertFalse(_has_unescaped_braces(content))

    def test_partner_no_unescaped_braces(self):
        content = Path(DOCS_DIR / "PartnerServer.md").read_text()
        self.assertFalse(_has_unescaped_braces(content))

    def test_aix_contains_url(self):
        content = Path(DOCS_DIR / "AIX.md").read_text()
        self.assertIn("`https://IPADDRESS-SERVERNAME:PORT/api/`", content)


if __name__ == "__main__":
    unittest.main()
