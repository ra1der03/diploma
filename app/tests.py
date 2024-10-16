import json
import unittest
import requests


class TestAPI(unittest.TestCase):

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    def test_register(self):
        headers = {
            'first_name': 'Harry', 'last_name': 'Potter', 'email': 'ra1der2020@yandex.ru', 'password': 'qwer1234A',
            'company': 'Hogwarts', 'position': 'Headmaster', 'contacts': json.dumps({
        "city": "Almaty",
        "street": "Shashkin street 4",
        "house": "Apartament 28",
        "structure": "123",
        "building": "123",
        "apartment": "123",
        "phone": "+49564563242"})
        }
        response = requests.post('http://localhost:8000/api/v1/user/register', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_AccountDetails(self):



if __name__ == '__main__':
    unittest.main()
