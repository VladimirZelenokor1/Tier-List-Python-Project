import unittest
from backend.security import hash_password, verify_password


class SecurityTestCase(unittest.TestCase):
    def test_hash_password(self):
        plaintext_password = "password123"
        hashed_password = hash_password(plaintext_password)
        self.assertTrue(hashed_password)

    def test_verify_password(self):
        plaintext_password = "password123"
        hashed_password = hash_password(plaintext_password)
        self.assertTrue(verify_password(plaintext_password, hashed_password))

        wrong_password = "wrongpassword"
        self.assertFalse(verify_password(wrong_password, hashed_password))


if __name__ == '__main__':
    unittest.main()
