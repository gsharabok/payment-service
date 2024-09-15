import unittest
from pydantic import ValidationError
from src.app.schemas import User, UserCreate, UserBalance

class TestSchemas(unittest.TestCase):

    def test_user_creation_valid(self):
        # Test valid user creation
        user_data = {
            "id": "123",
            "name": "Test User",
            "balance": 100.00
        }
        user = User(**user_data)
        self.assertEqual(user.id, "123")
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.balance, 100.00)

    def test_user_creation_invalid_balance(self):
        # Test invalid user creation (balance should be a Decimal)
        user_data = {
            "id": "123",
            "name": "Test User",
            "balance": "invalid_balance" 
        }
        with self.assertRaises(ValidationError) as context:
            User(**user_data)
        self.assertIn("Input should be a valid decimal", str(context.exception))

    def test_user_create_valid(self):
        # Test valid UserCreate schema
        user_create_data = {
            "id": "456",
            "name": "New User"
        }
        user_create = UserCreate(**user_create_data)
        self.assertEqual(user_create.id, "456")
        self.assertEqual(user_create.name, "New User")

    def test_user_balance_valid(self):
        # Test valid UserBalance schema
        user_balance_data = {
            "balance": 150.00
        }
        user_balance = UserBalance(**user_balance_data)
        self.assertEqual(user_balance.balance, 150.00)

    def test_user_balance_invalid(self):
        # Test invalid UserBalance schema (balance is required)
        with self.assertRaises(ValidationError) as context:
            UserBalance()
        self.assertIn("Field required", str(context.exception))

if __name__ == "__main__":
    unittest.main()