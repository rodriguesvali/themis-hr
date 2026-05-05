import os
import unittest
from unittest.mock import patch

from themis_hr_api.core.config import Settings


class SettingsTests(unittest.TestCase):
    def test_google_api_key_takes_precedence_over_gemini_api_key(self) -> None:
        with patch.dict(
            os.environ,
            {"GOOGLE_API_KEY": "google-key", "GEMINI_API_KEY": "gemini-key"},
            clear=True,
        ):
            with self.assertLogs("themis_hr_api.core.config", level="WARNING") as logs:
                settings = Settings(_env_file=None)

        self.assertEqual(settings.google_api_key, "google-key")
        self.assertIn("using GOOGLE_API_KEY", "\n".join(logs.output))

    def test_gemini_api_key_is_legacy_fallback(self) -> None:
        with patch.dict(os.environ, {"GEMINI_API_KEY": "gemini-key"}, clear=True):
            with self.assertLogs("themis_hr_api.core.config", level="WARNING") as logs:
                settings = Settings(_env_file=None)

        self.assertEqual(settings.google_api_key, "gemini-key")
        self.assertIn("legacy fallback", "\n".join(logs.output))


if __name__ == "__main__":
    unittest.main()
