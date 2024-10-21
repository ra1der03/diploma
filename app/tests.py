import json
import unittest
import requests


class TestAPI(unittest.TestCase):

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    # def test_register(self):
    #     payload = {
    #         "first_name": "Harry", "last_name": "Potter", "email": "ra1der2020@yandex.ru", "password": "qwer1234A",
    #         "company": "Hogwarts", "position": "Headmaster", "contacts": json.dumps({
    #     "city": "Almaty",
    #     "street": "Shashkin street 4",
    #     "house": "Apartament 28",
    #     "structure": "123",
    #     "building": "123",
    #     "apartment": "123",
    #     "phone": "+49564563242"})
    #     }
    #     headers = {'Content-type': 'application/json'}
    #     response = requests.post('http://localhost:8000/api/v1/user/register', headers=headers)
    #     self.assertEqual(response.status_code, 200)


    def test_confirm(self):
        payload = {"email": "ra1der2020@yandex.ru", "token": "7c84ee29609529971143e3df7dec5be0"}
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:8000/api/v1/user/register/confirm', data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_login(self):        
        payload = {
           'password': 'qwer1234A', 'email': 'ra1der2020@yandex.ru'}
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:8000/api/v1/user/login', data=json.dumps(payload), headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()
