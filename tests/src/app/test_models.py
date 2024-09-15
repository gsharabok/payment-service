import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models import Base, User, Transaction

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up an in-memory SQLite database for testing
        cls.engine = create_engine("sqlite:///:memory:")
        cls.Session = sessionmaker(bind=cls.engine)

        # Create all tables
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after tests
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        # Create a new session for each test
        self.session = self.Session()

    def tearDown(self):
        # Rollback the session after each test
        self.session.rollback()
        self.session.close()

    def test_user_creation(self):
        # Test creating a User instance
        user = User(id="123", name="Test User", balance=100.00)
        self.session.add(user)
        self.session.commit()

        # Query the user back
        queried_user = self.session.query(User).filter_by(id="123").first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.name, "Test User")
        self.assertEqual(queried_user.balance, 100.00)

    def test_transaction_creation(self):
        # Test creating a Transaction instance
        user = User(id="456", name="Another User", balance=200.00)
        self.session.add(user)
        self.session.commit()

        transaction = Transaction(
            user_id="456",
            amount=50.00,
            description="Test Transaction"
        )
        self.session.add(transaction)
        self.session.commit()

        # Query the transaction back
        queried_transaction = self.session.query(Transaction).filter_by(user_id="456").first()
        self.assertIsNotNone(queried_transaction)
        self.assertEqual(queried_transaction.amount, 50.00)
        self.assertEqual(queried_transaction.description, "Test Transaction")
        self.assertEqual(queried_transaction.user_id, "456")

if __name__ == "__main__":
    unittest.main()
