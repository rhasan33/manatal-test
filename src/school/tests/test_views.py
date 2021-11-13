from django.test import TestCase

from rest_framework.test import APIClient


class SchoolViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data1 = {
            'name': 'Some Random School',
            'number_of_seats': 20,
            'address': None
        }
        cls.data2 = {
            'name': 'Some Random School',
            'number_of_seats': 20,
            'available_seats': 30,
            'address': None
        }
        cls.data3 = {
            'name': 'Some Random School',
            'number_of_seats': "string",
            'available_seats': 30,
            'address': 'Some addresses'
        }
        cls.data4 = {
            'number_of_seats': "string",
            'available_seats': 30,
            'address': 'Some addresses'
        }
        cls.data5 = {
            'name': 'Some Random School',
            'available_seats': 30,
            'address': 'Some addresses'
        }
        cls.data6 = {
            'name': 'Some Random School',
            'number_of_seats': 10,
            'address': None
        }
        cls.data7 = {
            'name': 'Some Random School',
            'available_seats': 10,
            'address': None
        }
        cls._client = APIClient()
        cls._school_url = '/api/v1/schools/'

    def test_get_schools(self):
        response = self._client.get(self._school_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['meta_data'], dict)
        self.assertIsInstance(data['data'], list)

    def test_post_school(self):
        response = self._client.post(self._school_url, self.data1, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        response_data = data['data']
        self.assertEqual(data['success'], True)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response_data['number_of_seats'], response_data['available_seats'])

    def test_number_of_seats_and_available_seats(self):
        response = self._client.post(self._school_url, self.data2, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        response_data = data['data']
        self.assertEqual(data['success'], True)
        self.assertIsInstance(response_data, dict)
        self.assertEqual(response_data['number_of_seats'], response_data['available_seats'])

    def test_string_value_on_numbers(self):
        response = self._client.post(self._school_url, self.data3, format='json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['success'], False)

    def test_missing_name_value(self):
        response = self._client.post(self._school_url, self.data4, format='json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['success'], False)

    def test__missing_number_of_seats_value(self):
        response = self._client.post(self._school_url, self.data5, format='json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['success'], False)

    def test_incorrect_update_number_of_seats_value(self):
        response = self._client.post(self._school_url, self.data1, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        update_resp = self._client.put(f'{self._school_url}{data["data"]["id"]}/', self.data6, format='json')
        self.assertEqual(update_resp.status_code, 400)
        data = update_resp.json()
        self.assertEqual(data['success'], False)

    def test_incorrect_update_available_seats_value(self):
        response = self._client.post(self._school_url, self.data1, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        update_resp = self._client.put(f'{self._school_url}{data["data"]["id"]}/', self.data7, format='json')
        self.assertEqual(update_resp.status_code, 400)
        data = update_resp.json()
        self.assertEqual(data['success'], False)

    def test_incorrect_patch_available_seats_value(self):
        response = self._client.post(self._school_url, self.data1, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        update_resp = self._client.patch(f'{self._school_url}{data["data"]["id"]}/', self.data7, format='json')
        self.assertEqual(update_resp.status_code, 200)
        data = update_resp.json()
        self.assertEqual(data['success'], True)
        self.assertNotEqual(self.data7['available_seats'], data['data']['available_seats'])

    def test_pagination(self):
        for _ in range(20):
            self._client.post(self._school_url, self.data1, format='json')
        response = self._client.get(self._school_url + '?page_size=5')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['data']), 5)
        self.assertEqual(data['meta_data']['count'], 20)

    def test_invalid_page_number(self):
        for _ in range(20):
            self._client.post(self._school_url, self.data1, format='json')
        response = self._client.get(self._school_url + '?page=5')
        self.assertEqual(response.status_code, 404)

