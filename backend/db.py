from pymongo import MongoClient
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Global client instance for connection reuse
_client = None
_db = None

def get_db():
    """Get database connection with proper error handling and connection reuse"""
    global _client, _db
    
    try:
        # Reuse existing connection if available
        if _client is not None and _db is not None:
            # Test the connection
            _client.admin.command('ping')
            return _db
    except Exception:
        # Connection is stale, reset
        _client = None
        _db = None
    
    try:
        # Create new connection
        _client = MongoClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test the connection
        _client.admin.command('ping')
        _db = _client.get_default_database()
        
        logger.info("Successfully connected to MongoDB")
        return _db
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        logger.warning("Using mock database - some features may be limited")
        
        # Return a mock database object for development
        return MockDatabase()

class MockDatabase:
    """Mock database for development when MongoDB is not available"""
    
    def __init__(self):
        self.users = MockCollection("users")
        self.contests = MockCollection("contests")
        self.reminders = MockCollection("reminders")
        logger.info("Using mock database")

class MockCollection:
    """Mock collection that simulates basic MongoDB operations"""
    
    def __init__(self, name):
        self.name = name
        self.data = {}
    
    def find_one(self, query=None):
        logger.debug(f"Mock {self.name}.find_one({query})")
        return None
    
    def find(self, query=None):
        logger.debug(f"Mock {self.name}.find({query})")
        return []
    
    def insert_one(self, document):
        logger.debug(f"Mock {self.name}.insert_one({document})")
        return type('MockResult', (), {'inserted_id': 'mock_id'})()
    
    def update_one(self, query, update, upsert=False):
        logger.debug(f"Mock {self.name}.update_one({query}, {update}, upsert={upsert})")
        return type('MockResult', (), {'modified_count': 1, 'upserted_id': None})()
    
    def delete_one(self, query):
        logger.debug(f"Mock {self.name}.delete_one({query})")
        return type('MockResult', (), {'deleted_count': 1})()
    
    def delete_many(self, query):
        logger.debug(f"Mock {self.name}.delete_many({query})")
        return type('MockResult', (), {'deleted_count': 0})()


