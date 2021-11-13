import random
from uuid import uuid4

from django.test import TestCase

from student.models import Student
from school.models import School


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(
            name='123@#UKqw()',
            number_of_seats=30,
            available_seats="30",
            address='Unit 6969 Box 8784\nDPO AA 50404'
        )

        cls.student1 = Student.objects.create(
            first_name='Rakib',
            last_name='Hasan',
            identifier=str(uuid4().hex)[:20],
            school=cls.school,
            nationality=random.choice(['thai', 'bangladeshi']),
            age='20'
        )

        cls.student2 = Student.objects.create(
            first_name='Rakib',
            last_name='Hasan',
            identifier=str(uuid4().hex)[:20],
            school=cls.school,
            nationality=random.choice(['thai', 'bangladeshi']),
            age='20'
        )

    def test_first_name_value(self):
        student = Student.objects.get(pk=self.student1.id)
        field_value = student.first_name
        self.assertEqual(field_value, 'Rakib')
        self.assertIsInstance(field_value, str)
        self.assertLessEqual(len(field_value), 150)

    def test_last_name_value(self):
        student = Student.objects.get(pk=self.student1.id)
        field_value = student.last_name
        self.assertEqual(field_value, 'Hasan')
        self.assertIsInstance(field_value, str)
        self.assertLessEqual(len(field_value), 150)

    def test_identifier_value(self):
        student1 = Student.objects.get(pk=self.student1.id)
        student2 = Student.objects.get(pk=self.student2.id)
        field1_value = student1.identifier
        field2_value = student2.identifier
        self.assertNotEqual(field1_value, field2_value)
        self.assertIsInstance(field1_value, str)
        self.assertEqual(len(field1_value), 20)
        self.assertEqual(len(field2_value), 20)
