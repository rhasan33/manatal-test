from django.test import TestCase

from rest_framework.test import APIClient

from school.models import School


class StudentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(
            name='Some Random School',
            number_of_seats=20,
            available_seats=20,
            address='Some address',
        )
        cls.school2 = School.objects.create(
            name='Some Random School',
            number_of_seats=1,
            available_seats=1,
            address='Some address',
        )
        cls.data1 = {
            'first_name': 'Maiden',
            'last_name': 'Surname',
            'school': cls.school.id,
            'nationality': 'thai',
            'age': 30,
        }
        cls.data2 = {
            'first_name': 'Maiden',
            'last_name': 'Surname',
            'nationality': 'thai',
            'age': 30,
        }
        cls.data3 = {
            'school': cls.school.id,
            'nationality': 'thai',
            'age': 30,
        }
        cls.data4 = {
            'school': cls.school2.id,
            'nationality': 'bangladeshi',
            'age': 20,
        }
        cls._client = APIClient()
        cls._student_url = '/api/v1/students/'

    def test_get_empty_students_list(self):
        response = self._client.get(self._student_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['meta_data'], dict)
        self.assertIsInstance(data['data'], list)

    def test_create_student(self):
        resp = self._client.post(self._student_url, self.data1, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['data'], dict)

    def test_student_create_without_school(self):
        resp = self._client.post(self._student_url, self.data2, format='json')
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertEqual(data['success'], False)

    def test_student_without_first_last_name(self):
        resp = self._client.post(self._student_url, self.data3, format='json')
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertEqual(data['success'], False)

    def test_student_create_for_school_seat_check(self):
        for _ in range(20):
            self._client.post(self._student_url, self.data1, format='json')
        school = School.objects.get(pk=self.school.id)
        self.assertEqual(school.available_seats, 0)
        resp = self._client.post(self._student_url, self.data1, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_update_student_with_school_change(self):
        resp = self._client.post(self._student_url, self.data1, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        upd_resp = self._client.patch(f'{self._student_url}{data["data"]["id"]}/', self.data4, format='json')
        self.assertEqual(upd_resp.status_code, 200)
        school1 = School.objects.get(pk=self.school.id)
        school2 = School.objects.get(pk=self.school2.id)
        self.assertEqual(school1.available_seats, 20)
        self.assertEqual(school2.available_seats, 0)


class StudentNestedViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(
            name='Some Random School',
            number_of_seats=20,
            available_seats=20,
            address='Some address',
        )
        cls.school2 = School.objects.create(
            name='Some Random School',
            number_of_seats=1,
            available_seats=1,
            address='Some address',
        )
        cls.data1 = {
            'first_name': 'Maiden',
            'last_name': 'Surname',
            'school': cls.school.id,
            'nationality': 'thai',
            'age': 30,
        }
        cls.data4 = {
            'school': cls.school2.id,
            'nationality': 'bangladeshi',
            'age': 20,
        }
        cls._client = APIClient()
        cls._student_url = f'/api/v1/schools/{cls.school.id}/students/'

    def test_get_empty_students_list(self):
        response = self._client.get(self._student_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['meta_data'], dict)
        self.assertIsInstance(data['data'], list)

    def test_create_student(self):
        resp = self._client.post(self._student_url, self.data1, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['data'], dict)

    def test_update_student_with_school_change(self):
        resp = self._client.post(self._student_url, self.data1, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        upd_resp = self._client.patch(f'{self._student_url}{data["data"]["id"]}/', self.data4, format='json')
        print(upd_resp.json())
        self.assertEqual(upd_resp.status_code, 200)
        school1 = School.objects.get(pk=self.school.id)
        school2 = School.objects.get(pk=self.school2.id)
        self.assertEqual(school1.available_seats, 20)
        self.assertEqual(school2.available_seats, 0)

    def test_student_create_for_school_seat_check(self):
        for _ in range(20):
            self._client.post(self._student_url, self.data1, format='json')
        school = School.objects.get(pk=self.school.id)
        self.assertEqual(school.available_seats, 0)
        resp = self._client.post(self._student_url, self.data1, format='json')
        self.assertEqual(resp.status_code, 400)
