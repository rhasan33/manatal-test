from django.db import models

from manatal.models import BaseModel


class School(BaseModel):
    name = models.CharField(max_length=200)
    number_of_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    class Meta:
        db_table = 'schools'

    def __str__(self) -> str:
        return str(self.name)
