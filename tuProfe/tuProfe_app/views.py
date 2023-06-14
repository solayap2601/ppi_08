# Importa la funcion render para renderizar las plantillas
from django.shortcuts import render
# Importa los modelos necesarios  de la pagina
from .models import Docente, Materia, Calificacion, Comentario, Usuario, Autorizacion
# Importa  para operaciones matematicas
import math  
# Importa Q para realizar consultas complejas en la base de datos
from django.db.models import Q  
# Importa HttpResponse para manejar respuestas HTTP
from django.http import HttpResponse  
 # Importa make_password para cifrar contraseñas
from django.contrib.auth.hashers import make_password 
# Importa  para enviar correos electronicos
from django.core.mail import send_mail  
# Importa render y redirect para renderizar y redirigir a vistas
from django.shortcuts import render, redirect  
# Importa funciones de autenticacion y inicio de sesion
from django.contrib.auth import authenticate, login as auth_login  
# Importa login_required para requerir inicio de sesion
from django.contrib.auth.decorators import login_required  
# Importa el modelo User de autenticacion de Django
from django.contrib.auth.models import User  
# Importa csrf_exempt para desactivar proteccion CSRF en vistas especificas

from django.views.decorators.csrf import csrf_exempt  
# Importa el modulo json para trabajar con datos JSON
import json
 # Importa el módulo re para realizar expresiones regulares  
import re 
# Importa messages para mostrar mensajes de error o éxito al usuario
from django.contrib import messages 
from django.contrib.auth.models import User
    #funcion del registro del usuario

# Create your views here.
def home(request):
    # Renderiza la plantilla 'home.html' y la devuelve como respuesta
    return render(request, 'home.html') 


def register(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        
        # Valida y registra un nuevo usuario
        if not correo.endswith('@unal.edu.co'):
            messages.error(request, 'No estás usando un correo válido')
        elif User.objects.filter(email=correo).exists():
            messages.error(request, 'Ya existe un usuario registrado con ese correo electrónico')
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
            # Crea y guarda un nuevo usuario
            user = User.objects.create_user(username=correo, email=correo, password=contrasena)
            user.first_name = nombre
            user.save()
            return redirect('login')  # Redirige al usuario a la página de inicio de sesión
    
    return render(request, 'register.html')  # Renderiza la plantilla 'register.html' y la devuelve como respuesta

# Vista de inicio de sesion
def login(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Autentica al usuario
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Inicia sesion
            auth_login(request, user)  
            # Redirige al usuario a la pagina de inicio
            return redirect('home')  
        else:
            error_message = 'Correo electronico o contraseña incorrectos'
    
    context = {'error_message': error_message}
    # Renderiza la plantilla 'login.html' con el contexto y la devuelve como respuesta
    return render(request, 'login.html', context)  
    #funcion para calificar
def calificar(request):
    docente = request.POST.get("docente")
    materia = request.POST.get("materia")
    
    docente = Docente.objects.get(id=docente)
    materia = Materia.objects.get(id=materia)
    
    plantilla = render(request, "calificar.html", {"docente": docente, "materia": materia})
    # Renderiza la plantilla 'calificar.html' con los datos y la devuelve como respuesta
    return plantilla 
    
    #funcion guardar
def guardar(request):
    docente = request.POST.get("docente")
    materia = request.POST.get("materia")
    manejo = request.POST.get("manejo")
    metodologia = request.POST.get("metodologia")
    general = request.POST.get("general")
    comentario = request.POST.get("comentario")

    usuario = User.objects.get(id=request.user.id)
    docente = Docente.objects.get(id=docente)
    materia = Materia.objects.get(id=materia)

    aut = Autorizacion.objects.filter(email_estudiante = request.user.email, materia = materia, docente = docente)
    aut.delete()


    calificacion = Calificacion(usuario=usuario, docente=docente, materia=materia, general=general, metodologia=metodologia, manejo_tema=manejo)
    comentario = Comentario(usuario=usuario, docente=docente, materia=materia, texto=comentario)
    calificacion.save()
    comentario.save()

    response = redirect('/buscar/')
    # Redirige al usuario a la pagina de busqueda
    return response  
    
    #funcion de busqueda
def buscar(request):
    busqueda = request.GET.get("busqueda")
    id_materia = request.GET.get("materia")

    if busqueda == None:
        busqueda = 0

    if id_materia == None:
        id_materia = 0

    # Realiza la busqueda de materias basada en los parametros recibidos
    materias = Materia.objects.filter(Q(nombre__contains=busqueda) | Q(facultad__contains=busqueda))

    if id_materia != 0:
        docentes = Materia.objects.get(id=id_materia).docentes.all()
        lista_calificaciones = []
        
        # Calcula la calificacion promedio para cada docente de la materia seleccionada
        for c in docentes:
            calificaciones = Calificacion.objects.filter(docente_id=c.id, materia_id=id_materia)
            general = 0
            for j in calificaciones:
                general += j.general
            if calificaciones.count() == 0:
                general = "No hay datos"
            else:
                general = general / calificaciones.count()
            lista_calificaciones.append(general)
    else:
        docentes = 0
        lista_calificaciones = []

    plantilla = render(request, "buscar.html", {"docentes": docentes, "materias": materias, "busqueda": busqueda, "lista_calificaciones": lista_calificaciones, "id_materia": id_materia})
    return plantilla  # Renderiza la plantilla 'buscar.html' con los datos y la devuelve como respuesta
    
    #funcion en la cual estan los docente
def docente(request, id_docente, id_materia, pagina):
    calificaciones = Calificacion.objects.filter(docente_id=id_docente, materia_id=id_materia)
    general = 0
    metodologia = 0
    manejo_tema = 0

    for i in calificaciones:
        general += i.general
        metodologia += i.metodologia
        manejo_tema += i.manejo_tema

    if calificaciones.count() == 0:
        general = "No hay datos"
        metodologia = "No hay datos"
        manejo_tema = "No hay datos"
    else:
        general = general / calificaciones.count()
        metodologia = metodologia / calificaciones.count()
        manejo_tema = manejo_tema / calificaciones.count()

    comentarios = Comentario.objects.filter(docente_id=id_docente, materia_id=id_materia)
    max_pag = math.ceil(comentarios.count() / 3)
    if max_pag == 0:
        max_pag = 1
    indice = (pagina - 1) * 3

    if(request.user.is_authenticated):
        if(Autorizacion.objects.filter(email_estudiante = request.user.email, materia = Materia.objects.get(id=id_materia), docente = Docente.objects.get(id=id_docente)).exists()):
            authorized = 1
        else:
            authorized = 0
    else:
        authorized = 0

    plantilla = render(request, "docente.html", {"docente": Docente.objects.get(id=id_docente), "materia": Materia.objects.get(id=id_materia), "general": general, "metodologia": metodologia, "manejo_tema": manejo_tema, "comentarios": comentarios[indice:indice + 3], "pagina": pagina, "max_pag": max_pag, "authorized":authorized})
    # Renderiza la plantilla 'docente.html' con los datos y la devuelve como respuesta
    return plantilla  

def politicasp(request):
    # Renderiza la plantilla 'politicasp.html' y la devuelve como respuesta
    return render(request, 'politicasp.html')  
