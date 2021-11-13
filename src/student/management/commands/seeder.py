import random
from uuid import uuid4

import faker.providers
from django.core.management.base import BaseCommand

from faker import Faker

from school.models import School
from student.models import Student

NATIONALITIES = (
    'thai',
    'bangladeshi'
)

SCHOOLS = (
    'Rifles Public School',
    'Aaga Khan School',
    'Scholastica School'
)


class Provider(faker.providers.BaseProvider):
    def nationalities(self) -> str:
        return self.random_element(NATIONALITIES)

    def schools(self) -> str:
        return self.random_element(SCHOOLS)


class Command(BaseCommand):
    help = 'Seeding data using faker'

    def handle(self, *args, **options):
        fake_data = Faker(['en_TH'])
        fake_data.add_provider(Provider)

        for _ in range(1, 5):
            number_of_seats = random.randint(15, 30)
            school = School.objects.create(
                name=fake_data.schools(),
                number_of_seats=number_of_seats,
                available_seats=number_of_seats,
                address=fake_data.address()
            )
            for _ in range (1, random.randint(1, number_of_seats)):
                Student.objects.create(
                    first_name=fake_data.first_name(),
                    last_name=fake_data.last_name(),
                    identifier=str(uuid4().hex)[:20],
                    school=school,
                    nationality=fake_data.nationalities(),
                    age=random.randint(1, 80)
                )
        self.stdout.write(self.style.SUCCESS('database seed done'))



