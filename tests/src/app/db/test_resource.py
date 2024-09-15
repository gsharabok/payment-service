import unittest
from sqlalchemy.ext.asyncio import create_async_engine
from src.app.db.resource import create_session
import typing

class TestCreateSession(unittest.IsolatedAsyncioTestCase):

    async def test_create_session(self):
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        session = create_session(engine)
        self.assertIsInstance(session, typing.AsyncIterator)

if __name__ == '__main__':
    unittest.main()