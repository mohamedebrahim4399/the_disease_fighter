import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'api_test'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'mohamed', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.new_patient = {
            "name": "Alice",
            "email": "alice@mail.com",
            "password": "123456",
            "phone": "982341345",
            "location": "USA",
            "gender": "Male",
            "about": "Hey, I'm Alice",
            "dob": "09/09/1990"
        }

        self.new_doctor = {
            "name": "Jean",
            "email": "jean@mail.com",
            "password": "12345",
            "phone": "3490324932",
            "clinic_location": "Cairo",
            "gender": "Female",
            "about": "Hello, I'm Dr.Jean",
            "dob": "05/03/1885",
            "spec_id": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    def test_get_specializations(self):
        res = self.client().get('/specializations')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['specializations'])
        self.assertTrue(len(data['specializations']))





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()