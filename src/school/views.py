from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from school.models import School
from school.serializers import SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolSerializer
    permission_classes = (AllowAny,)
    queryset = School.objects.filter()
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        # check the request body for number_of_seats
        if not request.data.get('number_of_seats'):
            raise ValidationError('number_of_seats is required', code=status.HTTP_400_BAD_REQUEST)
        # check the request body for data type and value
        if not isinstance(request.data['number_of_seats'], int) or request.data['number_of_seats'] <= 0:
            raise ValidationError(detail='number_of_seats must not positive integer value',
                                  code=status.HTTP_400_BAD_REQUEST)
        request.data['available_seats'] = request.data['number_of_seats']
        return super(SchoolViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                school = School.objects.select_for_update().get(pk=kwargs[self.lookup_field])
            except School.DoesNotExist:
                raise ValidationError(detail='school not found', code=status.HTTP_404_NOT_FOUND)
            if request.data.get('number_of_seats') and request.data['number_of_seats'] < school.available_seats:
                raise ValidationError(detail='number of seats must be greater than available seat')
            request.data['available_seats'] = school.available_seats
            return super(SchoolViewSet, self).update(request, *args, **kwargs)
