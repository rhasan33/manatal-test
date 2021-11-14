from uuid import uuid4

from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from school.models import School
from student.models import Student
from student.serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)
    queryset = Student.objects.select_related('school').filter()
    search_fields = ['first_name', 'last_name']

    def create(self, request, *args, **kwargs):
        if not request.data.get('school'):
            raise ValidationError(detail='school is required', code=status.HTTP_400_BAD_REQUEST)
        request.data['identifier'] = str(uuid4().hex)[:20]
        with transaction.atomic():
            try:
                school = School.objects.select_for_update().get(pk=request.data['school'])
            except School.DoesNotExist:
                raise ValidationError(detail='school not found', code=status.HTTP_404_NOT_FOUND)
            if not school.available_seats:
                raise ValidationError(detail='school does not have available seat', code=status.HTTP_409_CONFLICT)
            school.remove_seat()
            return super(StudentViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # start of db transaction context
        with transaction.atomic():
            try:
                student = Student.objects.select_related('school').select_for_update().get(
                    pk=kwargs[self.lookup_field])
            except Student.DoesNotExist:
                raise ValidationError(detail='student not found', code=status.HTTP_404_NOT_FOUND)
            student.school.add_seat()
            return super(StudentViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # start of db transaction context
        with transaction.atomic():
            try:
                # fetch related data from db and lock the row
                student = Student.objects.select_related('school').select_for_update().get(pk=kwargs[self.lookup_field])
            except Student.DoesNotExist:
                raise ValidationError(detail='student not found', code=status.HTTP_404_NOT_FOUND)
            if request.data.get('school') and request.data['school'] != student.school.id:
                try:
                    school = School.objects.select_for_update().get(pk=request.data['school'])
                except School.DoesNotExist:
                    raise ValidationError(detail='school not found', code=status.HTTP_404_NOT_FOUND)
                # check if the new school has any available seat
                if not school.available_seats:
                    raise ValidationError(detail='school does not have available seat', code=status.HTTP_409_CONFLICT)
                # remove one seat from the new school
                school.remove_seat()
                # add one seat to the previous school
                student.school.add_seat()
            return super(StudentViewSet, self).update(request, *args, **kwargs)


class StudentNestedViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return Student.objects.select_related('school').filter(school=self.kwargs['school_pk'])

    def get_object(self):
        try:
            return Student.objects.select_related('school').get(school=self.kwargs['school_pk'], pk=self.kwargs['pk'])
        except Student.DoesNotExist:
            raise ValidationError(detail='student not found', code=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        request.data['identifier'] = str(uuid4().hex)[:20]
        with transaction.atomic():
            try:
                school = School.objects.select_for_update().get(pk=kwargs['school_pk'])
                request.data['school'] = school.id
            except School.DoesNotExist:
                raise ValidationError(detail='school not found', code=status.HTTP_404_NOT_FOUND)
            if not school.available_seats:
                raise ValidationError(detail='school does not have available seat', code=status.HTTP_409_CONFLICT)
            school.remove_seat()
            return super(StudentNestedViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # start of db transaction context
        with transaction.atomic():
            try:
                student = Student.objects.select_related('school').select_for_update().get(
                    pk=kwargs[self.lookup_field])
            except Student.DoesNotExist:
                raise ValidationError(detail='student not found', code=status.HTTP_404_NOT_FOUND)
            student.school.add_seat()
            return super(StudentNestedViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # start of db transaction context
        with transaction.atomic():
            try:
                # fetch related data from db and lock the row
                student = Student.objects.select_related('school').select_for_update().get(
                    pk=kwargs[self.lookup_field], school=kwargs['school_pk']
                )
            except Student.DoesNotExist:
                raise ValidationError(detail='student not found', code=status.HTTP_404_NOT_FOUND)
            if request.data.get('school') and request.data['school'] != student.school.id:
                try:
                    school = School.objects.select_for_update().get(pk=request.data['school'])
                except School.DoesNotExist:
                    raise ValidationError(detail='school not found', code=status.HTTP_404_NOT_FOUND)
                # check if the new school has any available seat
                if not school.available_seats:
                    raise ValidationError(detail='school does not have available seat', code=status.HTTP_409_CONFLICT)
                # remove one seat from the new school
                school.remove_seat()
                # add one seat to the previous school
                student.school.add_seat()
            return super(StudentNestedViewSet, self).update(request, *args, **kwargs)


