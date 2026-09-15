import os
import unittest
from pathlib import Path

from telegram_toolkit.utils.config import check_config_exists, get_credentials, load_config, save_config


class TestConfig(unittest.TestCase):
    """Tests for credential configuration."""

    def setUp(self):
        self.config = Path("config.data")
        self.env = Path(".env")
        self.config_bak = Path("config.data.test-bak")
        self.env_bak = Path(".env.test-bak")
        for path in (self.config_bak, self.env_bak):
            path.unlink(missing_ok=True)
        if self.config.exists():
            self.config.rename(self.config_bak)
        if self.env.exists():
            self.env.rename(self.env_bak)

    def tearDown(self):
        for path in (self.config, self.env):
            path.unlink(missing_ok=True)
        if self.config_bak.exists():
            self.config_bak.rename(self.config)
        if self.env_bak.exists():
            self.env_bak.rename(self.env)

    def test_check_config_requires_valid_credentials(self):
        self.assertFalse(check_config_exists())
        self.config.write_text("[cred]\nid=12345\nhash=testhash\nphone=+123456789\n", encoding="utf-8")
        self.assertTrue(check_config_exists())

    def test_save_and_load_config(self):
        save_config("12345", "abcdef1234567890", "+1234567890")
        self.assertTrue(self.config.exists())
        self.assertTrue(self.env.exists())
        config = load_config()
        self.assertEqual(config["cred"]["id"], "12345")
        self.assertEqual(config["cred"]["hash"], "abcdef1234567890")
        self.assertEqual(config["cred"]["phone"], "+1234567890")
        self.assertEqual(get_credentials(), ("12345", "abcdef1234567890", "+1234567890"))

    def test_invalid_api_id_is_rejected(self):
        with self.assertRaises(ValueError):
            save_config("not-a-number", "hash", "+1234567890")


if __name__ == "__main__":
    unittest.main()
