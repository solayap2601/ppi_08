from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Curso, Usuario

def mi_vista(request):
    return HttpResponse("Hola, mundo!")

def index(request):
    return render(request, 'index.html', {'message': 'Bienvenido a la aplicación de calificación de profesores!'})


# Create your views here.
