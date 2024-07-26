import unittest
from app import app, db
from models import Message

class MessageServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_message(self):
        response = self.app.post('/create', json={
            "account_id": "1",
            "message_id": "123e4567-e89b-12d3-a456-426614174000",
            "sender_number": "1234567890",
            "receiver_number": "0987654321"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_messages(self):
        self.app.post('/create', json={
            "account_id": "1",
            "message_id": "123e4567-e89b-12d3-a456-426614174000",
            "sender_number": "1234567890",
            "receiver_number": "0987654321"
        })
        response = self.app.get('/get/messages/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_search_messages(self):
        self.app.post('/create', json={
            "account_id": "1",
            "message_id": "123e4567-e89b-12d3-a456-426614174000",
            "sender_number": "1234567890",
            "receiver_number": "0987654321"
        })
        response = self.app.get('/search?message_id=123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

if __name__ == '__main__':
    unittest.main()
