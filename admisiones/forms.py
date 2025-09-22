from django import forms
from .models import Multimedia, MensajeContacto, Testimonio, Hijo, PadreHijo, Usuario, Tarea, Calificacion

class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ['titulo', 'descripcion', 'archivo', 'tipo']

class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo electrónico'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }
from django import forms
from .models import Testimonio
class TestimonioForm(forms.ModelForm):
    class Meta:
        model = Testimonio
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu testimonio aquí...', 'maxlength': 500}),
        }
from .models import Hijo, PadreHijo

from django import forms
from .models import Usuario, Hijo, PadreHijo, Tarea, Calificacion

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_entrega', 'grado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'grado': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['tarea', 'hijo', 'nota', 'observaciones']
        widgets = {
            'tarea': forms.Select(attrs={'class': 'form-control'}),
            'hijo': forms.Select(attrs={'class': 'form-control'}),
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
class RegistroHijoForm(forms.ModelForm):
    class Meta:
        model = Hijo
        fields = ['nombre', 'fecha_nacimiento', 'grado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'grado': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para comprobante de pago bancario
from .models import ComprobantePago

class ComprobantePagoForm(forms.ModelForm):
    class Meta:
        model = ComprobantePago
        fields = ['monto', 'fecha_pago', 'comprobante']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        return nombre

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        from datetime import date
        if fecha and fecha > date.today():
            raise forms.ValidationError('La fecha de nacimiento no puede ser en el futuro.')
        return fecha

class LoginUsuarioForm(forms.Form):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class NotificacionForm(forms.ModelForm):
    class Meta:
        from .models import Notificacion
        model = Notificacion
        fields = ['titulo', 'contenido', 'tipo', 'destinatario']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'destinatario': forms.Select(attrs={'class': 'form-control'}),
        }

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'rol', 'telefono', 'direccion']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')
        if not username or len(username) < 4:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 4 caracteres.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password or len(password) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        return password
from django import forms
from .models import GaleriaImagen

class GaleriaImagenForm(forms.ModelForm):
    class Meta:
        model = GaleriaImagen
        fields = ['titulo', 'imagen', 'descripcion', 'etiquetas']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'etiquetas': forms.TextInput(attrs={'class': 'form-control'}),
        }
from django import forms
from django.utils import timezone
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin',
            'lugar', 'tipo', 'imagen', 'enlace_mas_info'
        ]
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for datetime fields
        now = timezone.now()
        if not self.instance.pk:  # New event
            # Set default start time to next hour
            next_hour = (now.replace(minute=0, second=0, microsecond=0) + 
                        timezone.timedelta(hours=1))
            self.initial['fecha_inicio'] = next_hour.strftime('%Y-%m-%dT%H:%M')
            # Set default end time to 2 hours after start
            self.initial['fecha_fin'] = (next_hour + timezone.timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio."
            )
            
        return cleaned_data
