# tuProfe URL Configuration

# El `urlpatterns` lista las URLs y las asocia a las vistas correspondientes.
# Para obtener mas informacion, consulta la documentacion de Django:
# https://docs.djangoproject.com/en/4.1/topics/http/urls/

# Importa de Django
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

# Esta parte Importa la vista
from tuProfe_app.views import (
    home, calificar, buscar, docente, guardar, login, register, politicasp
)

# Contiene todas las rutas (URLs) disponibles en la aplicacion
urlpatterns = [
    # Ruta para acceder a la interfaz de administración de Django.
    path('admin/', admin.site.urls),
    # Ruta para la pagina de inicio
    path('', home, name='home'),
    # Ruta de politicas y privacidad para la pagina
    path('politicasp/', politicasp, name='politicasp'),  
    # Ruta para el registro de usuarios
    path('registro/', register, name='registro'),  
    # Ruta de inicio de sesion
    path('login/', login, name='login'),  
    # Ruta de calificacion
    path('calificar/', calificar, name='calificar'),  
    # Ruta de busqueda de la pagina
    path('buscar/', buscar, name='buscar'),  
    # Ruta para mirar los docentes
    path('docente/<int:id_docente>/<int:id_materia>/<int:pagina>/', docente),
    # Ruta para guardar la calificacion
    path('guardar/', guardar, name='guardar'),  
    # Ruta de cerrar sesion en la pagina
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 
]
