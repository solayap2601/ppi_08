from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Curso, Usuario

def mi_vista(request):
    return HttpResponse("Hola, mundo!")



# Create your views here.
