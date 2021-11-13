from django.db import models

from manatal.models import BaseModel


class School(BaseModel):
    name = models.CharField(max_length=200)
    number_of_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    address = models.TextField(null=True)

    class Meta:
        db_table = 'schools'

    def __str__(self) -> str:
        return str(self.name)

    def remove_seat(self):
        self.available_seats -= 1
        self.save()

    def add_seat(self):
        self.available_seats += 1
        self.save()
