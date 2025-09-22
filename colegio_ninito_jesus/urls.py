from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('admisiones.urls', 'admisiones'), namespace='admisiones')),
    path('evaluaciones/', include('evaluations.urls', namespace='evaluations')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # Ruta eliminada para evitar conflicto de nombres con el namespace 'admisiones'
    path('area/matematicas/', views.area_matematicas, name='area_matematicas'),
    path('area/ciencias/', views.area_ciencias, name='area_ciencias'),
    path('area/espanol/', views.area_espanol, name='area_espanol'),
    path('area/sociales/', views.area_sociales, name='area_sociales'),
    path('area/tecnologia/', views.area_tecnologia, name='area_tecnologia'),
    path('area/pastoral/', views.area_pastoral, name='area_pastoral'),
    path('area/idiomas/', views.area_idiomas, name='area_idiomas'),
    path('area/psicologia/', views.area_psicologia, name='area_psicologia'),
    path('area/artes/', views.area_artes, name='area_artes'),
    path('area/deportes/', views.area_deportes, name='area_deportes'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)