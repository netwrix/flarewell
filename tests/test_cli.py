import subprocess
import sys
import os
import unittest
import shutil
from pathlib import Path

ERROR_MESSAGES = [
    "Could not parse expression with acorn",
    "Unexpected character `=`",
    "Unexpected end of file in expression",
    "Can't parse URL https://IPADDRESS-SERVERNAME:PORT/api/ with base unspecified://",
]


def run_flarewell():
    """Run the flarewell stub script used for testing."""
    cmd = [os.path.join('tests', 'flarewell'), '--input-dir', 'tests/input_docs', '--output-dir', 'tests/test_website/docs']
    return subprocess.run(cmd, capture_output=True, text=True)


class FlarewellTests(unittest.TestCase):
    def setUp(self):
        self.output_dir = Path('tests/test_website/docs')
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_flarewell_conversion_no_errors(self):
        result = run_flarewell()
        print(result.stdout)
        print(result.stderr)
        self.assertEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        for msg in ERROR_MESSAGES[:-1]:
            self.assertNotIn(msg, output)

    def test_npm_build_no_errors(self):
        conv = run_flarewell()
        self.assertEqual(conv.returncode, 0)
        result = subprocess.run(['npm', 'run', 'build'], cwd='tests/test_website', capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        self.assertEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertNotIn(ERROR_MESSAGES[-1], output)


if __name__ == '__main__':
    unittest.main()
