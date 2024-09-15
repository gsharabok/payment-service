import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from src.app.api.payments import ROUTER
from src.app import schemas

class TestPaymentsAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(ROUTER)

    @patch('src.app.api.payments.get_payment_repo')
    async def test_create_user(self, mock_get_payment_repo):
        mock_payment_repo = AsyncMock()
        mock_get_payment_repo.return_value = mock_payment_repo

        user_data = {
            "id": "123",
            "name": "Test User"
        }

        mock_payment_repo.create_user.return_value = schemas.User(**user_data)

        response = self.client.post("/user/", json=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), user_data)

    @patch('src.app.api.payments.get_payment_repo')
    async def test_get_user_balance(self, mock_get_payment_repo):
        mock_payment_repo = AsyncMock()
        mock_get_payment_repo.return_value = mock_payment_repo

        user_id = "123"
        balance_data = {"balance": 100.00}
        mock_payment_repo.get_user_balance.return_value = 100.00

        response = self.client.get(f"/user/{user_id}/balance/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), balance_data)

    @patch('src.app.api.payments.get_payment_repo')
    async def test_get_user_balance_not_found(self, mock_get_payment_repo):
        mock_payment_repo = AsyncMock()
        mock_get_payment_repo.return_value = mock_payment_repo

        user_id = "nonexistent"
        mock_payment_repo.get_user_balance.return_value = None

        response = self.client.get(f"/user/{user_id}/balance/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

if __name__ == "__main__":
    unittest.main()