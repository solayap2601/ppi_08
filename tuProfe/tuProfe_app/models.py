# Importa el modulo models de Django para definir modelos de base de datos
from django.db import models 
# Importa el modelo User de Django para trabajar con usuarios del sistema
from django.contrib.auth.models import User 


class Docente(models.Model):
    # Campo para almacenar el nombre del docente
    nombre = models.CharField(max_length=50)
    # Campo para almacenar el correo electronico del docente
    correo = models.EmailField(max_length=50)
    # Campo para almacenar la ubicacion de la oficina del docente
    oficina = models.CharField(max_length=50)

    def __str__(self):
        # Devuelve una representacion legible del objeto Docente
        return self.nombre


class Materia(models.Model):
    # Campo para almacenar el nombre de la materia
    nombre = models.CharField(max_length=50)
    # Campo para almacenar el nombre de la facultad de la materia
    facultad = models.CharField(max_length=50)
    # Relacion ManyToMany con el modelo Docente
    docentes = models.ManyToManyField(Docente)

    def __str__(self):
        # Devuelve una representacion legible del objeto Materia
        return self.nombre


class Usuario(models.Model):
    # Campo para almacenar el nombre del usuario
    nombre = models.CharField(max_length=50)
    # Campo para almacenar el correo electronico del usuario
    correo = models.EmailField(max_length=50)
    # Campo para almacenar la contraseña del usuario
    contrasena = models.CharField(max_length=100)

    def __str__(self):
        # Devuelve una representacion legible del objeto Usuario
        return self.nombre


class Comentario(models.Model):
    # Relacion ForeignKey con el modelo User de Django
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Relacion ForeignKey con el modelo Docente
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    # Relacion ForeignKey con el modelo Materia
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    # Campo para almacenar el texto del comentario
    texto = models.CharField(max_length=500)

    def __str__(self):
        # Devuelve una representacion legible del objeto Comentario
        return self.docente.nombre + " - " + self.materia.nombre


class Calificacion(models.Model):
    # Relacion ForeignKey con el modelo User de Django
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Relacion ForeignKey con el modelo Docente
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    # Relacion ForeignKey con el modelo Materia
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    # Campo para almacenar la calificacion general
    general = models.PositiveIntegerField()
    # Campo para almacenar la calificacion de metodologia
    metodologia = models.PositiveIntegerField()
    # Campo para almacenar la calificacion de manejo del tema
    manejo_tema = models.PositiveIntegerField()

    def __str__(self):
        # Devuelve una representacion legible del objeto Calificacion
        return self.docente.nombre + " - " + self.materia.nombre
