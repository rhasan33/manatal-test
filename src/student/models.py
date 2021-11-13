from django.db import models

from manatal.models import BaseModel


class Student(BaseModel):
    class NationalityChoices(models.TextChoices):
        THAI = 'thai', 'thai'
        BANGLADESHI = 'bangladeshi', 'bangladeshi'

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    identifier = models.CharField(max_length=20, unique=True)
    school = models.ForeignKey(to='school.School', on_delete=models.PROTECT, related_name='school')
    nationality = models.CharField(max_length=11, choices=NationalityChoices.choices, default=NationalityChoices.THAI)
    age = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'students'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
