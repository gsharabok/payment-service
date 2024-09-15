import unittest
from src.app.settings import Settings

class TestSettings(unittest.TestCase):

    def test_default_settings(self):
        # Create an instance of Settings
        settings = Settings()

        # Check default values
        self.assertEqual(settings.service_name, "Payment Service")
        self.assertEqual(settings.app_host, "0.0.0.0")
        self.assertEqual(settings.app_port, 8000)
        self.assertFalse(settings.debug)
        self.assertEqual(settings.log_level, "info")

    def test_settings_with_env(self):
        # Test loading settings from environment variables
        import os
        os.environ["SERVICE_NAME"] = "Test Service"
        os.environ["APP_HOST"] = "127.0.0.1"
        os.environ["APP_PORT"] = "8080"
        os.environ["DEBUG"] = "true"
        os.environ["LOG_LEVEL"] = "debug"

        settings = Settings()

        self.assertEqual(settings.service_name, "Test Service")
        self.assertEqual(settings.app_host, "127.0.0.1")
        self.assertEqual(settings.app_port, 8080)
        self.assertTrue(settings.debug)
        self.assertEqual(settings.log_level, "debug")

        # Clean up environment variables
        del os.environ["SERVICE_NAME"]
        del os.environ["APP_HOST"]
        del os.environ["APP_PORT"]
        del os.environ["DEBUG"]
        del os.environ["LOG_LEVEL"]

if __name__ == "__main__":
    unittest.main()