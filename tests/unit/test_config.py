import unittest
from backend.config import Settings


class TestSettings(unittest.TestCase):
    def test_default_values(self):
        settings = Settings()

        self.assertEqual(settings.secret,
                         "effd59a38c8593085c62f9c6d6e87fcbe9633e85ef16c52f")
        self.assertEqual(settings.database_uri, "sqlite:///app.db")
        self.assertEqual(settings.token_url, "/auth/token")

    def test_custom_values(self):
        custom_secret = "custom_secret_key"
        custom_database_uri = "postgresql://user:password@localhost:5432/mydb"
        custom_token_url = "/custom/token"

        settings = Settings(
            secret=custom_secret,
            database_uri=custom_database_uri,
            token_url=custom_token_url,
        )

        self.assertEqual(settings.secret, custom_secret)
        self.assertEqual(settings.database_uri, custom_database_uri)
        self.assertEqual(settings.token_url, custom_token_url)


if __name__ == '__main__':
    unittest.main()
