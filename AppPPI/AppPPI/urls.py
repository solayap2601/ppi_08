"""AppPPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Tu_profe.views import login_view, register_view, facultades_view, carrera_view, asignatura_view, profesor_view, search_view, calificar, perfil 

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('facultades/', facultades_view, name='facultades'),
    path('carrera/<int:carrera_id>/', carrera_view, name='carrera'),
    path('asignatura/<int:asignatura_id>/', asignatura_view, name='asignatura'),
    path('profesor/<int:profesor_id>/<int:curso_id>/', profesor_view, name='profesor'),
    path('search/', search_view, name='search'),
    path('calificar/<int:profesor_id>/<int:curso_id>/', calificar, name='calificar'),
    path('perfil/', perfil, name='perfil'),
]


