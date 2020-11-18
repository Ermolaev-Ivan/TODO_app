from main import app
from unittest import TestCase

from flask import json


class MyTestCase(TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        result = self.app.get('/api/task/')
        print(result)

    # рабочий запрос
    # curl -d '{"title": "test", "content": "con_test"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/task/

    def test_post(self):    # пока не работает
        data = {
            'title': 'test',
            'content': 'con_test'
        }
        a_json = json.dumps(data)
        result = self.app.post('/api/task/')
        print(result)
