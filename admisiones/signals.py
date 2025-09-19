from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name='Profesores')
    Group.objects.get_or_create(name='Padres')
