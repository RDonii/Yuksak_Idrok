import os
import unittest
from app import create_app
from models.models import create_db
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import json

load_dotenv()


class YITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "yi_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            os.getenv('USER'), os.getenv('PASSWORD'), 'localhost:5432', self.database_name)
        create_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # barcha jadvallarni yaratish
            self.db.create_all()

    def tearDown(self):
        """Men test uchun alohida database ochdim (yi_test).
        Agar test uchun ham production uchun ishlatilinadigan database dan foydalanmoqchi bo'lsangiz (yi),
        testdan so'ng database ma'lumotlarini asil holiga qaytaruvchi code shu yerda yoziladi.
        """
        pass

    def test_a_get_course_by_id(self):
        res = self.client().get('/categories/9999')
        data  = json.loads(res.data)

        
