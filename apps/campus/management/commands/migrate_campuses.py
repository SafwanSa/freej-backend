from django.core.management.base import BaseCommand, CommandError
from apps.campus.models import *
import itertools as it


class Command(BaseCommand):
    help = 'Adds dummy data.'

    def handle(self, *args, **options):

        kfupm = Campus.objects.get(name_en='KFUPM')

        buildings_range = range(813, 864)
        rooms_range1 = range(101, 130)
        rooms_range2 = range(201, 230)
        rooms_range3 = range(301, 330)

        for i in buildings_range:
            building = Building.objects.create(
                campus=kfupm,
                name=str(i)
            )
            for j in it.chain(rooms_range1, rooms_range2, rooms_range3):
                room = Room.objects.create(
                    building=building,
                    name=str(j)
                )

        result = ''
        self.stdout.write(self.style.SUCCESS(result))
