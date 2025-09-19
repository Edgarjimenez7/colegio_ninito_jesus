from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def configurar_permisos_grupos(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from admisiones.models import Tarea, Calificacion, Hijo, PadreHijo

    # Profesores: pueden ver, agregar y modificar tareas y calificaciones
    profesores, _ = Group.objects.get_or_create(name='Profesores')
    tareas_ct = ContentType.objects.get_for_model(Tarea)
    calificaciones_ct = ContentType.objects.get_for_model(Calificacion)
    profesores.permissions.set([
        Permission.objects.get(codename='add_tarea', content_type=tareas_ct),
        Permission.objects.get(codename='change_tarea', content_type=tareas_ct),
        Permission.objects.get(codename='view_tarea', content_type=tareas_ct),
        Permission.objects.get(codename='add_calificacion', content_type=calificaciones_ct),
        Permission.objects.get(codename='change_calificacion', content_type=calificaciones_ct),
        Permission.objects.get(codename='view_calificacion', content_type=calificaciones_ct),
    ])

    # Padres: pueden ver hijos, padre-hijo y calificaciones
    padres, _ = Group.objects.get_or_create(name='Padres')
    hijos_ct = ContentType.objects.get_for_model(Hijo)
    padre_hijo_ct = ContentType.objects.get_for_model(PadreHijo)
    padres.permissions.set([
        Permission.objects.get(codename='view_hijo', content_type=hijos_ct),
        Permission.objects.get(codename='view_padrehijo', content_type=padre_hijo_ct),
        Permission.objects.get(codename='view_calificacion', content_type=calificaciones_ct),
    ])
