from django.db import models

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField(max_length=1000)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.nombre} - {self.email} ({self.fecha_envio:%d/%m/%Y %H:%M})"
from django.db import models

from django.conf import settings

class ComprobantePago(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    comprobante = models.FileField(upload_to='comprobantes/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Comprobante de Pago'
        verbose_name_plural = 'Comprobantes de Pago'
        ordering = ['-fecha_subida']

    def __str__(self):
        return f"{self.autor.get_full_name()} - {self.monto} ({self.fecha_pago})"

class Testimonio(models.Model):
    autor = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    contenido = models.TextField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.autor} - {self.contenido[:30]}..."

# Modelo para galería multimedia
class Multimedia(models.Model):
    TIPO_CHOICES = (
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    )
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='galeria/')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"
from django.db import models

# Modelo para tareas asignadas por profesores
class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    profesor = models.ForeignKey('admisiones.Usuario', on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'})
    grado = models.CharField(max_length=50)  # Grado al que va dirigida la tarea

    def __str__(self):
        return f"{self.titulo} ({self.grado})"

# Modelo para calificaciones asignadas por profesores a hijos
class Calificacion(models.Model):
    tarea = models.ForeignKey('admisiones.Tarea', on_delete=models.CASCADE)
    hijo = models.ForeignKey('admisiones.Hijo', on_delete=models.CASCADE)
    profesor = models.ForeignKey('admisiones.Usuario', on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'})
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    observaciones = models.TextField(blank=True)
    fecha_asignada = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.hijo.nombre} - {self.tarea.titulo}: {self.nota}"
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('padre', 'Padre'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='padre')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admisiones_usuario_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admisiones_usuario_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"

# Modelo para hijos
class Hijo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    grado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Relación entre padre e hijo
class PadreHijo(models.Model):
    padre = models.ForeignKey('admisiones.Usuario', on_delete=models.CASCADE, limit_choices_to={'rol': 'padre'})
    hijo = models.ForeignKey('admisiones.Hijo', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.padre.username} - {self.hijo.nombre}"
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    contenido = models.TextField()
    imagen_principal = models.ImageField(upload_to='noticias/')
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destacada = models.BooleanField(default=False)
    etiquetas = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'

class Evento(models.Model):
    TIPO_CHOICES = [
        ('academico', 'Académico'),
        ('deportivo', 'Deportivo'),
        ('cultural', 'Cultural'),
        ('religioso', 'Religioso'),
        ('otro', 'Otro'),
    ]
    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='otro')
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    enlace_mas_info = models.URLField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            self.slug = base_slug
            counter = 1
            while Evento.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    @property
    def esta_activo(self):
        now = timezone.now()
        return self.fecha_inicio <= now <= self.fecha_fin
    
    @property
    def es_proximo(self):
        return self.fecha_inicio > timezone.now()
    
    @classmethod
    def proximo_evento(cls):
        return cls.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio').first()
    
    @classmethod
    def eventos_proximos(cls, limit=5):
        return cls.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio')[:limit]
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('aviso', 'Aviso'),
        ('mensaje', 'Mensaje'),
        ('alerta', 'Alerta'),
    ]
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='aviso')
    destinatario = models.ForeignKey('admisiones.Usuario', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.destinatario.username}"

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

class GaleriaImagen(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='galeria/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)
    etiquetas = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Imagen de Galería'
        verbose_name_plural = 'Galería de Imágenes'
from django.db import models
