import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from package_release import PACKAGE, decide, valid_version


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'test')
        self.git('config', 'user.email', 'test@example.invalid')
        PACKAGE.mkdir(parents=True)
        self.write_version('1.0.0')

    def tearDown(self):
        os.chdir(self.previous)
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.check_output(['git', *args], stderr=subprocess.STDOUT, text=True)

    def write_version(self, version):
        (PACKAGE / 'package.json').write_text(json.dumps({'name': 'com.coolishbee.google-signin', 'version': version}))
        self.git('add', '.')
        self.git('commit', '-qm', version)

    def decision(self, version=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return decide(version)

    def test_new_version(self):
        self.assertEqual(self.decision(), {'version': '1.0.0', 'tag': 'upm/v1.0.0', 'create': 'true', 'publish': 'true'})

    def test_existing_version_and_retry(self):
        self.git('tag', 'upm/v1.0.0')
        self.assertEqual(self.decision()['publish'], 'false')
        self.write_version('1.0.1')
        self.assertEqual(self.decision()['create'], 'true')
        retry = self.decision('1.0.0')
        self.assertEqual(retry['create'], 'false')
        self.assertEqual(retry['publish'], 'true')

    def test_missing_retry_tag(self):
        with self.assertRaises(ValueError):
            self.decision('1.0.0')

    def test_mismatched_tag(self):
        self.git('tag', 'upm/v2.0.0')
        with self.assertRaises(AssertionError):
            self.decision('2.0.0')

    def test_invalid_versions(self):
        for value in ['1.0', '01.0.0', '1.0.0+build', '1.0.0-01', '$(id)', '../x', '1.0.0\ntag=x']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                valid_version(value)
        self.assertEqual(valid_version('1.0.0-preview.1'), '1.0.0-preview.1')


if __name__ == '__main__':
    unittest.main()
