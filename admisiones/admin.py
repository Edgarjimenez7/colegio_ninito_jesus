from django.contrib import admin
from .models import MensajeContacto

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'email', 'fecha_envio', 'leido')
	list_filter = ('leido', 'fecha_envio')
	search_fields = ('nombre', 'email', 'mensaje')
from .models import Testimonio
admin.site.register(Testimonio)
from .models import Usuario
from .models import Hijo, PadreHijo, Tarea, Calificacion, Evento, Notificacion, Noticia, Multimedia

admin.site.register(Usuario)
admin.site.register(Hijo)
admin.site.register(PadreHijo)
admin.site.register(Tarea)
admin.site.register(Calificacion)
admin.site.register(Evento)
admin.site.register(Notificacion)
admin.site.register(Noticia)
admin.site.register(Multimedia)

from .models import ComprobantePago

@admin.register(ComprobantePago)
class ComprobantePagoAdmin(admin.ModelAdmin):
	list_display = ('autor', 'monto', 'fecha_pago', 'fecha_subida', 'aprobado')
	list_filter = ('aprobado', 'fecha_pago')
	search_fields = ('autor__username', 'monto')
	readonly_fields = ('fecha_subida',)
