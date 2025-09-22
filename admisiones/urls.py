from django.urls import path
from .views import (
    NoticiaListView, NoticiaDetailView, NoticiaCreateView, 
    EventoListView, EventoDetailView, EventoCreateView, EventoUpdateView, EventoDeleteView,
    InicioView, institucional, galeria_multimedia, calendario_escolar, testimonios, recursos, mapa, padres_estudiantes, registro_usuario, login_usuario, registrar_hijo,
    crear_tarea, asignar_calificacion, lista_tareas_profesor, lista_calificaciones_profesor, tareas_grado_padre, calificaciones_hijos_padre,
    calificaciones_redirect, tareas_redirect, panel_profesor, recuperar_contrasena, crear_notificacion, panel_usuario, reset_password
)
from .views import dashboard_panel_admin, GaleriaMultimediaView, testimonios_view, comprobante_pago_view, pagos_en_linea_view, contacto_view
from django.conf import settings
from django.conf.urls.static import static

app_name = 'admisiones'

urlpatterns = [
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('panel-usuario/', panel_usuario, name='panel_usuario'),
    path('notificaciones/crear/', crear_notificacion, name='crear_notificacion'),
    path('recuperar-contrasena/', recuperar_contrasena, name='recuperar_contrasena'),
    path('panel-profesor/', panel_profesor, name='panel_profesor'),
    path('contacto/', contacto_view, name='contacto'),
    path('padres-estudiantes/', padres_estudiantes, name='padres_estudiantes'),
    path('mapa/', mapa, name='mapa'),
    path('recursos/', recursos, name='recursos'),
    path('testimonios/', testimonios_view, name='testimonios'),
    path('calendario/', calendario_escolar, name='calendario_escolar'),
    path('galeria/', GaleriaMultimediaView.as_view(), name='galeria'),
    # Home
    path('', InicioView.as_view(), name='inicio'),
    
    # Noticias
    path('noticias/', NoticiaListView.as_view(), name='lista_noticias'),
   path('noticias/nueva/', NoticiaCreateView.as_view(), name='nueva_noticia'),
    path('noticias/<int:pk>/', NoticiaDetailView.as_view(), name='noticia_detalle'),
    path('noticias/<slug:slug>/', NoticiaDetailView.as_view(), name='noticia_detalle_slug'),
    
    # Eventos
    path('eventos/', EventoListView.as_view(), name='lista_eventos'),
    path('eventos/crear/', EventoCreateView.as_view(), name='crear_evento'),
    path('eventos/<slug:slug>/', EventoDetailView.as_view(), name='evento_detalle'),
    path('eventos/editar/<slug:slug>/', EventoUpdateView.as_view(), name='editar_evento'),
    path('eventos/eliminar/<slug:slug>/', EventoDeleteView.as_view(), name='eliminar_evento'),
    
    # Galería
    
    # Otras páginas
    path('historia/', institucional, name='historia'),
    path('mision/', institucional, name='mision'),
    # Registro de usuario
    path('registro/', registro_usuario, name='registro_usuario'),
    # Login personalizado
    path('login/', login_usuario, name='login_usuario'),
    # Registro de hijos
    path('registrar-hijo/', registrar_hijo, name='registrar_hijo'),
    # Tareas y calificaciones
    path('tareas/crear/', crear_tarea, name='crear_tarea'),
    path('tareas/asignar-calificacion/', asignar_calificacion, name='asignar_calificacion'),
    path('tareas/mis-tareas/', lista_tareas_profesor, name='lista_tareas_profesor'),
    path('tareas/mis-calificaciones/', lista_calificaciones_profesor, name='lista_calificaciones_profesor'),
    path('tareas/grado/', tareas_grado_padre, name='tareas_grado_padre'),
    path('tareas/calificaciones/', calificaciones_hijos_padre, name='calificaciones_hijos_padre'),
    # Rutas cortas para calificaciones y tareas
    path('calificaciones/', calificaciones_redirect, name='calificaciones_redirect'),
    path('tareas/', tareas_redirect, name='tareas_redirect'),
    path('vision/', institucional, name='vision'),
    path('institucional/', institucional, name='institucional'),
    path('catalogo-libros/', institucional, name='catalogo_libros'),
    path('dashboard-admin/', dashboard_panel_admin, name='dashboard_panel_admin'),
    path('pagos-en-linea/', pagos_en_linea_view, name='pagos_en_linea'),
    path('comprobante-pago/', comprobante_pago_view, name='comprobante_pago'),
        path('contacto/', contacto_view, name='contacto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)