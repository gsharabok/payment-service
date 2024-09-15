import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import Depends
from src.app.settings import Settings
from src.app.application import AppBuilder, application
from src.app.models import Base
from src.app.db.resource import create_session
import asyncio
from src.app.api.base import get_db
from fastapi import FastAPI


class TestApplication(unittest.TestCase):
    @patch('src.app.application.Settings')
    @patch('src.app.application.async_sessionmaker')
    @patch('src.app.application.create_async_engine')
    def setUp(self, mock_create_async_engine, mock_async_sessionmaker, mock_settings):
        # Mock the settings
        self.mock_settings = mock_settings.return_value
        self.mock_settings.db_dsn = "sqlite+aiosqlite:///:memory:"
        self.mock_settings.debug = True
        self.mock_settings.service_name = "Test Service"
        
        # Mock the async engine and session maker
        self.mock_engine = MagicMock()
        mock_create_async_engine.return_value = self.mock_engine
        self.mock_session_maker = MagicMock()
        mock_async_sessionmaker.return_value = self.mock_session_maker
        
        # Create an instance of AppBuilder
        self.app_builder = AppBuilder()

    def test_app_initialization(self):
        self.assertIsInstance(self.app_builder.app, FastAPI)
        self.assertEqual(self.app_builder.app.title, "Test Service")
        self.assertTrue(self.app_builder.app.debug)




# ////////////////////

# connection_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
# engine = create_async_engine(connection_url)
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# class TestApplication(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Mock the Settings
#         cls.settings_patcher = patch('src.app.application.Settings')
#         cls.mock_settings = cls.settings_patcher.start()
#         cls.mock_settings.return_value = Settings(
#             db_dsn="sqlite+aiosqlite:///:memory:",
#             debug=True,
#             app_port=8000,  # Use a test port
#             log_level="DEBUG"
#         )
        
#         # Create a new AppBuilder instance with mocked settings
#         cls.app_builder = AppBuilder()
#         cls.app_builder.settings = cls.mock_settings.return_value
        
#         # Initialize async resources
#         asyncio.run(cls.app_builder.init_async_resources())
        
#         # Build the application
#         cls.app = cls.app_builder.app
        
#         # Create a test client
#         cls.client = TestClient(cls.app)

#         # cls.db_session_maker = Depends(get_db)

#     @classmethod
#     def tearDownClass(cls):
#         # Stop the patcher
#         cls.settings_patcher.stop()
        
#         # Clean up async resources
#         asyncio.run(cls.app_builder.tear_down())

#     # def setUp(self):
#     #     # Create all tables before each test
#     #     asyncio.run(self.create_tables())

#     # def tearDown(self):
#     #     # Drop all tables after each test
#     #     asyncio.run(self.drop_tables())

#     # async def create_tables(self):
#         # async with self.app_builder.engine.begin() as conn:
#         # async with self.app_builder.get_async_session_maker() as session:
#         #     async with session.begin():
#         #         await session.run_sync(Base.metadata.create_all)


#     # async def drop_tables(self):
#     #     # async with self.app_builder.engine.begin() as conn:
#     #     async with self.app_builder.get_async_session_maker() as session:
#     #         async with session.begin():
#     #             await session.run_sync(Base.metadata.drop_all)


#     def test_app_routes(self):
#         routes = [route for route in application.routes]
#         for route in routes:
#             print(f"Route: {route.path}, methods: {route.methods}")
#         self.assertTrue(any(route.path == "/api/user/" for route in routes))

#     def test_create_user(self):
#         response = self.client.post(
#             "/api/user/",
#             json={"id": "127", "name": "Test User"}
#         )
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data["id"], "127")
#         self.assertEqual(data["name"], "Test User")
#         self.assertIn("balance", data)

#     def test_get_user_balance(self):
#         # First, create a user
#         create_response = self.client.post(
#             "/api/user/",
#             json={"id": "128", "name": "Test User"}
#         )
#         self.assertEqual(create_response.status_code, 200)
#         user_id = create_response.json()["id"]

#         # Get the user's balance
#         balance_response = self.client.get(f"/api/user/{user_id}/balance")
#         self.assertEqual(balance_response.status_code, 200)
#         balance_data = balance_response.json()
#         self.assertIn("balance", balance_data)

# if __name__ == "__main__":
#     unittest.main()


# ////////////////////

# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import StaticPool

# from src.app.application import AppBuilder
# from src.app.models import Base
# from src.app.settings import Settings

# # Override the database URL for testing
# @pytest.fixture(scope="module")
# def test_settings():
#     return Settings(db_dsn="sqlite+aiosqlite:///:memory:")

# @pytest.fixture(scope="module")
# def app(test_settings):
#     app_builder = AppBuilder()
#     app_builder.settings = test_settings
#     return app_builder.app

# @pytest.fixture(scope="module")
# def client(app):
#     return TestClient(app)

# @pytest.fixture(scope="module")
# async def async_session_maker(test_settings):
#     engine = create_async_engine(
#         str(test_settings.db_dsn),
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     async_session_maker = sessionmaker(
#         engine, class_=AsyncSession, expire_on_commit=False
#     )
#     yield async_session_maker

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

# @pytest.mark.asyncio
# async def test_create_user(client, async_session_maker):
#     response = client.post(
#         "/api/user/",
#         json={"id": "123", "name": "Test User"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == "123"
#     assert data["name"] == "Test User"
#     assert "balance" in data

# @pytest.mark.asyncio
# async def test_get_user_balance(client, async_session_maker):
#     # First, create a user
#     create_response = client.post(
#         "/api/users/",
#         json={"username": "balanceuser", "email": "balance@example.com", "full_name": "Balance User"}
#     )
#     assert create_response.status_code == 200
#     user_id = create_response.json()["id"]

#     # Now, get the user's balance
#     balance_response = client.get(f"/api/users/{user_id}/balance")
#     assert balance_response.status_code == 200
#     balance_data = balance_response.json()
#     assert "balance" in balance_data
#     assert balance_data["balance"] == 0  # Assuming initial balance is 0

# @pytest.mark.asyncio
# async def test_health_check(client):
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}

# ////////////

# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import (
#     async_sessionmaker,
#     create_async_engine,
#     AsyncSession as AsyncSessionType,
#     AsyncEngine,
# )

# # from main import app, get_db
# from src.app.application import AppBuilder, application
# # from database import Base
# from src.app.models import Base
# from src.app.api.base import get_db


# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def override_get_db():
#     return TestingSessionLocal
#     # try:
#     #     db = TestingSessionLocal()
#     #     yield db
#     # finally:
#     #     db.close()


# @pytest.fixture()
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)

# application.dependency_overrides[get_db] = override_get_db

# client = TestClient(application)


# # def test_get_todos(test_db):
# #     response = client.post("/todos/", json={"text": "some new todo"})
# #     data1 = response.json()
# #     response = client.post("/todos/", json={"text": "some even newer todo"})
# #     data2 = response.json()

# #     assert data1["user_id"] == data2["user_id"]

# #     response = client.get("/todos/")

# #     assert response.status_code == 200
# #     assert response.json() == [
# #         {"id": data1["id"], "user_id": data1["user_id"], "text": data1["text"]},
# #         {"id": data2["id"], "user_id": data2["user_id"], "text": data2["text"]},
# #     ]


# def test_get_empty_todos_list(test_db):
#     response = client.post(
#         "/api/user/",
#         json={"id": "126", "name": "Test User"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == "126"
#     assert data["name"] == "Test User"
#     # self.assertIn("balance", data)