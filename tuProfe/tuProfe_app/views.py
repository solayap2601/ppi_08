from django.shortcuts import render
from .models import Docente, Materia, Calificacion, Comentario, Usuario
import math
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import re
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        if not correo.endswith('@unal.edu.co'):
            messages.error(request, 'No estás usando un correo válido')
        elif len(contrasena) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
        elif not re.search(r'[A-Z]', contrasena):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula')
        elif not re.search(r'[a-z]', contrasena):
            messages.error(request, 'La contraseña debe contener al menos una letra minúscula')
        elif not re.search(r'\d', contrasena):
            messages.error(request, 'La contraseña debe contener al menos un número')
        elif not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?]', contrasena):
            messages.error(request, 'La contraseña debe contener al menos un carácter especial')
        else:
            usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena)
            usuario.save()
            return redirect('home')
    return render(request, 'register.html')


def login(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Correo electrónico o contraseña incorrectos'
    context = {'error_message': error_message}
    return render(request, 'login.html', context)


@login_required
def calificar(request):
	docente = request.GET.get("docente")
	materia = request.GET.get("materia")
	docente = Docente.objects.get(id=docente)
	materia = Materia.objects.get(id=materia)
	plantilla = render(request,"calificar.html",{"docente":docente, "materia":materia})
	return plantilla
	if not request.user.is_authenticated:
		return redirect('login')

def guardar(request):
	docente = request.GET.get("docente")
	materia = request.GET.get("materia")
	manejo = request.GET.get("manejo")
	metodologia = request.GET.get("metodologia")
	general = request.GET.get("general")
	comentario = request.GET.get("comentario")

	usuario = Usuario.objects.get(id=1)
	docente = Docente.objects.get(id=docente)
	materia = Materia.objects.get(id=materia)

	calificacion = Calificacion(usuario= usuario,docente= docente, materia= materia, general= general, metodologia= metodologia, manejo_tema= manejo)
	comentario = Comentario(usuario= usuario,docente= docente, materia= materia, texto= comentario)
	calificacion.save()
	comentario.save()
	response = redirect('/buscar/')
	return response

def buscar(request):


	busqueda = request.GET.get("busqueda")
	id_materia = request.GET.get("materia")

	if(busqueda == None):
		busqueda = 0

	if(id_materia == None):
		id_materia = 0
	
	materias = Materia.objects.filter(Q(nombre__contains=busqueda) | Q(facultad__contains =busqueda))
	if(id_materia!=0):
		docentes = Materia.objects.get(id=id_materia).docentes.all()

		lista_calificaciones=[]
		for c in docentes:
			calificaciones = Calificacion.objects.filter(docente_id = c.id, materia_id = id_materia)
			general = 0
			for j in calificaciones:
				general += j.general
			if(calificaciones.count()==0):
				general = "No hay datos"
			else:
				general = general/calificaciones.count()
			lista_calificaciones.append(general)
	else:
		docentes = 0
		lista_calificaciones=[]

	plantilla = render(request,"buscar.html",{"docentes":docentes, "materias":materias, "busqueda":busqueda, "lista_calificaciones":lista_calificaciones, "id_materia":id_materia})
	return plantilla

def docente(request, id_docente,id_materia, pagina):

    calificaciones = Calificacion.objects.filter(docente_id = id_docente, materia_id = id_materia)
    general = 0
    metodologia = 0
    manejo_tema = 0

    for i in calificaciones:
    	general += i.general
    	metodologia += i.metodologia
    	manejo_tema += i.manejo_tema


    if(calificaciones.count()==0):
    	general = "No hay datos"
    	metodologia = "No hay datos"
    	manejo_tema = "No hay datos"
    else: 	
    	general = general/calificaciones.count()
    	metodologia = metodologia/calificaciones.count()
    	manejo_tema = manejo_tema/calificaciones.count()

    comentarios = Comentario.objects.filter(docente_id = id_docente, materia_id = id_materia)
    max_pag =math.ceil(comentarios.count()/3)
    if max_pag == 0:
    	max_pag = 1
    indice = (pagina-1)*3


    plantilla = render(request,"docente.html",{"docente":Docente.objects.get(id=id_docente), "materia":Materia.objects.get(id=id_materia), "general":general, "metodologia":metodologia, "manejo_tema":manejo_tema, "comentarios":comentarios[indice:indice+3], "pagina":pagina, "max_pag":max_pag})
    return plantilla