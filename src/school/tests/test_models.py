from datetime import datetime

from django.test import TestCase

from school.models import School


class SchoolModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(
            name='123@#UKqw()',
            number_of_seats=30,
            available_seats="30",
            address='Unit 6969 Box 8784\nDPO AA 50404'
        )

    def test_name_value(self):
        school = School.objects.get(pk=self.school.id)
        field_value = school.name
        self.assertEqual(field_value, '123@#UKqw()')
        self.assertIsInstance(field_value, str)
        self.assertLessEqual(len(field_value), 200)

    def test_number_of_seats_value(self):
        school = School.objects.get(pk=self.school.id)
        field_value = school.number_of_seats
        self.assertEqual(field_value, 30)
        self.assertIsInstance(field_value, int)

    def test_available_seats_value(self):
        school = School.objects.get(pk=self.school.id)
        field_value = school.available_seats
        self.assertEqual(field_value, 30)
        self.assertIsInstance(field_value, int)

    def test_address_value(self):
        school = School.objects.get(pk=self.school.id)
        field_value = school.address
        self.assertEqual(field_value, 'Unit 6969 Box 8784\nDPO AA 50404')
        self.assertIsInstance(field_value, str)

    def test_created_at(self):
        school = School.objects.get(pk=self.school.id)
        field_value = school.created_at
        self.assertIsInstance(field_value, datetime)
