from django.test import TestCase

from school.models import School
from school.serializers import SchoolSerializer


class SchoolSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(
            name='123@#UKqw()',
            number_of_seats=30,
            available_seats="30",
            address='Unit 6969 Box 8784\nDPO AA 50404'
        )
        cls.data = SchoolSerializer(cls.school).data

    def test_serializer_value(self):
        self.assertIsInstance(self.data['name'], str)
        self.assertIsInstance(self.data['number_of_seats'], int)
        self.assertIsInstance(self.data['available_seats'], int)
        self.assertIsInstance(self.data['address'], str)

