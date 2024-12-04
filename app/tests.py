import json
import unittest
import requests


# class TestRegisterAPI(unittest.TestCase):

#     def test_register(self):
#         payload = {"first_name": "имr4fef45",
#                    "last_name": "фамиwefлия54",
#                    "email": "kiryaka003@yandex.ru",
#                    "password": "qwer1234Aasd",
#                    "company": "5345",
#                    "position": "345345sdf"}
#         headers = {'Content-type': 'application/json'}
#         response = requests.post('http://localhost:8000/api/v1/user/register', headers=headers, data=json.dumps(payload))
#         print("register", response.text)
#         self.assertEqual(response.json().get('Status'), True)



class TestUserAPI(unittest.TestCase):


    # def test_confirm(self):
    #     payload = {"email": "kiryaka003@yandex.ru", "token": "e00f0fc28ee1ab2e507"}
    #     headers = {'Content-type': 'application/json'}
    #     response = requests.post('http://localhost:8000/api/v1/user/register/confirm', data=json.dumps(payload), headers=headers)
    #     print("confirm", response.text)
    #     self.assertEqual(response.status_code, 200)

    # def test_login(self):        
    #     payload = {
    #        'password': 'qwer1234Aasd', 'email': 'kiryaka003@yandex.ru'}
    #     headers = {'Content-type': 'application/json'}
    #     response = requests.post('http://localhost:8000/api/v1/user/login', data=json.dumps(payload), headers=headers)
    #     print("login", response.text)
    #     self.token = response.json().get('Token')
    #     self.assertEqual(response.json().get('Status'), True)

    # def test_contacts_create(self):
    #     payload = {
    #     "city": "Almaty",
    #     "street": "Shashkin street 40",
    #     "house": "Apartment 28",
    #     "structure": "123",
    #     "building": "123",
    #     "apartment": "123",
    #     "phone": "+49564563242"}
    #     headers ={'Content-type': 'application/json', 'Authorization': self.token}
    #     response = requests.post('http://localhost:8000/api/v1/user/contacts', data=json.dumps(payload), headers=headers)


