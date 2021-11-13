from typing import Dict

from rest_framework import serializers

from student.models import Student
from school.serializers import SchoolLiteSerializer


class StudentSerializer(serializers.ModelSerializer):
    school_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

    @staticmethod
    def get_school_info(obj: Student) -> Dict:
        return SchoolLiteSerializer(obj.school).data
