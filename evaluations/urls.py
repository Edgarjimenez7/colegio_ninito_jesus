from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('', views.TeacherListView.as_view(), name='teacher_list'),
    path('evaluar/<int:teacher_id>/', views.submit_evaluation, name='submit_evaluation'),
    path('gracias/', views.evaluation_thanks, name='evaluation_thanks'),
]