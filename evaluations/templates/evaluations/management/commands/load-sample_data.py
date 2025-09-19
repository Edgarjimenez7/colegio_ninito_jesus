from django.core.management.base import BaseCommand
from evaluations.models import Teacher

class Command(BaseCommand):
    help = 'Load sample teacher data'

    def handle(self, *args, **options):
        teachers = [
            {'name': 'Juan Pérez', 'subject': 'Matemáticas'},
            {'name': 'María García', 'subject': 'Ciencias'},
            {'name': 'Carlos López', 'subject': 'Español'},
            {'name': 'Ana Martínez', 'subject': 'Historia'},
        ]
        
        for teacher_data in teachers:
            Teacher.objects.get_or_create(**teacher_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample teacher data'))