from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('facultades/', views.facultades_view, name='facultades'),
    path('carrera/<int:carrera_id>/', views.carrera_view, name='carrera'),
    path('asignatura/<int:asignatura_id>/', views.asignatura_view, name='asignatura'),
    path('profesor/<int:profesor_id>/<int:curso_id>/', views.profesor_view, name='profesor'),
    path('search/', views.search_view, name='search'),
    path('calificar/<int:profesor_id>/<int:curso_id>/', views.calificar, name='calificar'),
    path('perfil/', views.perfil, name='perfil'),
]

