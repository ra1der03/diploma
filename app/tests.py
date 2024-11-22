import json
import unittest
import requests


class TestRegisterAPI(unittest.TestCase):

    def test_register(self):
        payload = {
            "first_name": "Harry", "last_name": "Potter", "email": "ra1der2018@yandex.ru", "password": "qwer1234A",
            "company": "Hogwarts", "position": "Headmaster"}
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://95.163.222.196/api/v1/user/register', headers=headers, data=json.dumps(payload))
        print("register", response.text)
        self.assertEqual(response.json().get('Status'), True)


    # def test_confirm(self):
    #     payload = {"email": "ra1der2020@yandex.ru", "token": ""}
    #     headers = {'Content-type': 'application/json'}
    #     response = requests.post('http://95.163.222.196/api/v1/user/register/confirm', data=json.dumps(payload), headers=headers)
    #     self.assertEqual(response.status_code, 200)


# class TestLoginAPI(unittest.TestCase):

#     def setUp(self):
#         print("method setUp")

#     def tearDown(self):
#         print("method tearDown")

#     def test_login(self):        
#         payload = {
#            'password': 'qwer1234A', 'email': 'ra1der5@yandex.ru'}
#         headers = {'Content-type': 'application/json'}
#         response = requests.post('http://95.163.222.196/api/v1/user/login', data=json.dumps(payload), headers=headers)
#         print("login", response.text)
#         self.token = response.json()['Token']
#         print("token", self.token)
#         self.assertEqual(response.status_code, 200)

    



if __name__ == '__main__':
    unittest.main()
