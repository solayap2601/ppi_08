from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Usuario, Facultad, Carrera, Asignatura, Profesor, Curso, Calificacion, Comentario


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('facultades')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        Usuario.objects.create_user(nombre=nombre, email=email, password=password)
        messages.success(request, 'Cuenta creada exitosamente.')
        return redirect('login')
    return render(request, 'register.html')


def facultades_view(request):
    facultades = Facultad.objects.all()
    return render(request, 'facultades.html', {'facultades': facultades})


def carrera_view(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id)
    asignaturas = Asignatura.objects.filter(carrera=carrera)
    return render(request, 'carrera.html', {'carrera': carrera, 'asignaturas': asignaturas})


def asignatura_view(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    profesores = Profesor.objects.filter(
        curso__asignatura=asignatura
    ).annotate(
        avg_rating=Avg('curso__calificacion__valor'),
        num_ratings=Count('curso__calificacion')
    )
    return render(request, 'asignatura.html', {'asignatura': asignatura, 'profesores': profesores})


def profesor_view(request, profesor_id, curso_id):
    profesor = get_object_or_404(Profesor, id=profesor_id)
    curso = get_object_or_404(Curso, id=curso_id, profesor=profesor)
    calificacion = Calificacion.objects.filter(
        curso=curso, profesor=profesor
    ).aggregate(
        Avg('valor')
    )
    comentarios = Comentario.objects.filter(curso=curso, profesor=profesor)
    return render(request, 'profesor.html', {
        'profesor': profesor,
        'curso': curso,
        'calificacion': calificacion,
        'comentarios': comentarios
    })


def search_view(request):
    query = request.GET.get('q')
    asignaturas = Profesor.objects.none()
    profesores = Profesor.objects.none()
    if query:
        asignaturas = Asignatura.objects.filter(nombre__icontains=query)
        profesores = Profesor.objects.filter(
            nombre__icontains=query
        ).annotate(
            avg_rating=Avg('curso__calificacion__valor'),
            num_ratings=Count('curso__calificacion')
        )
    return render(request, 'search.html', {
        'asignaturas': asignaturas,
        'profesores': profesores,
        'query': query
    })


# Vista para calificar un profesor en un curso específico
def calificar(request, profesor_id, curso_id):
    if request.method == 'POST':
        # Obtener la calificación y el comentario del formulario
        valor = request.POST['valor']
        comentario_texto = request.POST['comentario']
        
        # Obtener el usuario que está calificando
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        
        # Obtener el profesor y el curso correspondientes
        profesor = Profesor.objects.get(id=profesor_id)
        curso = Curso.objects.get(id=curso_id)
        
        # Crear la nueva calificación y el nuevo comentario
        calificacion = Calificacion.objects.create(valor=valor, curso=curso, profesor=profesor)
        comentario = Comentario.objects.create(texto=comentario_texto, curso=curso, profesor=profesor)
        
        # Agregar la calificación y el comentario al usuario
        usuario.calificaciones.add(calificacion)
        usuario.comentarios.add(comentario)
        
        return redirect('/perfil/')
    else:
        # Obtener el profesor y el curso correspondientes
        profesor = Profesor.objects.get(id=profesor_id)
        curso = Curso.objects.get(id=curso_id)
        
        return render(request, 'calificar.html', {'profesor': profesor, 'curso': curso})

# Vista para mostrar el perfil del usuario y sus calificaciones y comentarios
def perfil(request):
    # Obtener el usuario actual
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Obtener las calificaciones y comentarios del usuario
    calificaciones = usuario.calificaciones.all()
    comentarios = usuario.comentarios.all()
    
    return render(request, 'perfil.html', {'usuario': usuario, 'calificaciones': calificaciones, 'comentarios': comentarios})