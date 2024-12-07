import json
import unittest
import requests


class TestRegisterAPI(unittest.TestCase):

    def test_register(self):
        payload = {"first_name": "имr4fef45",
                   "last_name": "фамиwefлия54",
                   "email": "zlunny42@gmail.com",
                   "password": "qwer1234Aasd",
                   "company": "5345",
                   "position": "345345sdf"}
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:8000/api/v1/user/register', headers=headers, data=json.dumps(payload))
        print("register", response.text)
        self.assertEqual(response.json().get('Status'), True)



class TestUserAPI(unittest.TestCase):


    def test_confirm(self):
        payload = {"email": "kiryaka003@yandex.ru", "token": "e00f0fc28ee1ab2e507"}
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:8000/api/v1/user/register/confirm', data=json.dumps(payload), headers=headers)
        print("confirm", response.text)
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.base_url = 'http://localhost:8000/api/v1/user'
        self.login_payload = {
           'password': 'qwer1234Aasd', 'email': 'kiryaka003@yandex.ru'
        }
        self.headers = {'Content-type': 'application/json'}
        self.login()

    def login(self):
        response = requests.post(f'{self.base_url}/login', data=json.dumps(self.login_payload), headers=self.headers)
        self.token = response.json().get('Token')
        self.headers['Authorization'] = f'Token {self.token}'

    def test_login(self):
        response = requests.post(f'{self.base_url}/login', data=json.dumps(self.login_payload), headers=self.headers)
        self.assertEqual(response.json().get('Status'), True)

    def test_contacts_create(self):
        payload = {
            "city": "Almaty",
            "street": "Shashkin street 40",
            "house": "Apartment 28",
            "structure": "123",
            "building": "123",
            "apartment": "123",
            "phone": "+49564563242"
        }
        response = requests.post(f'{self.base_url}/contact', data=json.dumps(payload), headers=self.headers)
        self.assertEqual(response.json().get('Status'), True)

    def test_contacts_read(self):
        response = requests.get(f'{self.base_url}/contact', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        
    def test_contacts_delete(self):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Token {self.token}'}
        response = requests.get(f'{self.base_url}/contact', headers=headers)
        id = response.json()[0].get('id')
        response = requests.delete(f'{self.base_url}/contact', headers=headers, data=json.dumps({"items": str(id)}))
        self.assertEqual(response.json().get('Status'), True)

    def test_user_edit(self):
        headers = {'Content-type': 'application/json', 'Authorization' : f'Token {self.token}'}
        payload = {
        "first_name": "Имя",
        "last_name": "Фамилия",
        "email": "kiryaka003@yandex.ru",
        "password": "qwer1234Aasd",
        "company": "Yandex",
        "position": "Floor-cleaner"}
        response = requests.post(f'{self.base_url}/details', data=json.dumps(payload), headers=headers)
        self.assertEqual(response.json().get('Status'), True)
    
    def test_user_read(self):
        headers = {'Content-type': 'application/json', 'Authorization' : f'Token {self.token}'}
        response = requests.get(f'{self.base_url}/details', headers=headers)
        self.assertEqual(response.status_code, 200)


class TestPartnerAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://localhost:8000/api/v1'
        self.login_payload_shop = {
           'password': 'qwer1234Aasd', 'email': 'zlunny03@gmail.com'
        }
        self.login_payload_user = {
           'password': 'qwer1234Aasd', 'email': 'kiryaka003@yandex.ru'
        }
        self.headers_shop = {'Content-type': 'application/json'}
        self.headers_user = {'Content-type': 'application/json'}
        response_s = requests.post(f'{self.base_url}/user/login', data=json.dumps(self.login_payload_shop), headers=self.headers_shop)
        response_u = requests.post(f'{self.base_url}/user/login', data=json.dumps(self.login_payload_user), headers=self.headers_user)
        self.token_shop = response_s.json().get('Token')
        self.token_user = response_u.json().get('Token')
        self.headers_shop['Authorization'] = f'Token {self.token_shop}'
        self.headers_user['Authorization'] = f'Token {self.token_user}'

    def test_partner_update(self):
        payload = {'url': 'https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml'}
        response = requests.post(f'{self.base_url}/partner/update', data=json.dumps(payload), headers=self.headers_shop)
        self.assertEqual(response.json().get('Status'), True)

    def test_post_partner_state(self):
        payload = {'state': 'on'}
        response = requests.post(f"{self.base_url}/partner/state", data=json.dumps(payload), headers=self.headers_shop)
        self.assertEqual(response.status_code, 200)

    def test_get_partner_state(self):
        payload = {'url': 'https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml'}
        response = requests.get(f"{self.base_url}/partner/state", data=json.dumps(payload), headers=self.headers_shop)
        self.assertEqual(response.status_code, 200)

    def test_get_partner_orders(self):
        payload = {'url': 'https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml'}
        response = requests.get(f"{self.base_url}/partner/orders", data=json.dumps(payload), headers=self.headers_shop)
        self.assertEqual(response.status_code, 200)

    def test_get_shops(self):
        headers = {'Content-type': 'application/json'}
        response = requests.get(f"{self.base_url}/shops", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_products(self):
        headers = {'Content-type': 'application/json'}
        response = requests.get(f"{self.base_url}/products?shop_id=2&category_id=224", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_basket_add_product(self):
        data = {
        "items": json.dumps([ { "product_info": 426, "quantity": 13 }, { "product_info": 427, "quantity": 12, } ])} 
        response = requests.post(f"{self.base_url}/basket", data=json.dumps(data), headers=self.headers_user)  
        print(response.text) 
        self.assertEqual(response.json().get('Status'), True)   
    
    def test_basket_change_product(self):
        data = {
        "items": json.dumps([ { "product_info": 426, "quantity": 15 }, { "product_info": 427, "quantity": 1, } ])} 
        response = requests.put(f"{self.base_url}/basket", data=json.dumps(data), headers=self.headers_user)  
        print(response.text) 
        self.assertEqual(response.json().get('Status'), True)  

    def test_basket_del_product(self):
        data = {
        "items": "426"} 
        response = requests.delete(f"{self.base_url}/basket", data=json.dumps(data), headers=self.headers_user)  
        print(response.text) 
        self.assertEqual(response.json().get('Status'), True)  

    def test_basket_products(self):
        response = requests.get(f"{self.base_url}/basket",  headers=self.headers_user)  
        print(response.text) 
        self.assertEqual(response.status_code, 200)  

    def test_categories(self):
        response = requests.get(f"{self.base_url}/categories",  headers=self.headers_user)  
        self.assertEqual(response.status_code, 200)  

    def test_make_order(self):
        data = { "id": "19", "contact": "25"} 
        response = requests.post(f"{self.base_url}/order", data=json.dumps(data), headers=self.headers_user)  
        self.assertEqual(response.json().get('Status'), True) 

    def test_get_orders(self):
        response = requests.get(f"{self.base_url}/order", headers=self.headers_user)  
        self.assertEqual(response.status_code, 200) 