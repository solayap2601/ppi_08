from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Docente(models.Model):
	nombre = models.CharField(max_length=50)
	correo = models.EmailField(max_length=50)
	oficina = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre

class Materia(models.Model):
	nombre = models.CharField(max_length=50)
	facultad = models.CharField(max_length=50)
	docentes = models.ManyToManyField(Docente)

	def __str__(self):
		return self.nombre

class Usuario(models.Model):
	nombre = models.CharField(max_length=50)
	correo = models.EmailField(max_length=50)
	contrasena = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre

class Comentario(models.Model):
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)
	docente = models.ForeignKey(Docente, on_delete = models.CASCADE)
	materia = models.ForeignKey(Materia, on_delete = models.CASCADE)
	texto = models.CharField(max_length=500)

	def __str__(self):
		return self.docente.nombre + " - " + self. materia.nombre

class Calificacion(models.Model):
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)
	docente = models.ForeignKey(Docente, on_delete = models.CASCADE)
	materia = models.ForeignKey(Materia, on_delete = models.CASCADE)
	general = models.PositiveIntegerField()
	metodologia = models.PositiveIntegerField()
	manejo_tema = models.PositiveIntegerField()

	def __str__(self):
		return self.docente.nombre + " - " + self. materia.nombre

