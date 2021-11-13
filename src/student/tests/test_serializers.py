import random
from uuid import uuid4

from django.test import TestCase

from student.models import Student
from school.models import School
from student.serializers import StudentSerializer


class StudentSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(
            name='123@#UKqw()',
            number_of_seats=30,
            available_seats="30",
            address='Unit 6969 Box 8784\nDPO AA 50404'
        )

        cls.student = Student.objects.create(
            first_name='Rakib',
            last_name='Hasan',
            identifier=str(uuid4().hex)[:20],
            school=cls.school,
            nationality=random.choice(['thai', 'bangladeshi']),
            age='20'
        )
        cls.data = StudentSerializer(cls.student).data

    def test_serializer_value(self):
        self.assertIsInstance(self.data['first_name'], str)
        self.assertIsInstance(self.data['last_name'], str)
        self.assertIsInstance(self.data['identifier'], str)
        self.assertIsInstance(self.data['school'], int)
        self.assertIsInstance(self.data['school_info'], dict)
        self.assertIsInstance(self.data['nationality'], str)
        self.assertIsInstance(self.data['age'], int)

