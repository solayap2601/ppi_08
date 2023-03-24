from django.db import models

class Facultad(models.Model):
    nombre = models.CharField(max_length=50)

class Carrera(models.Model):
    nombre = models.CharField(max_length=50)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)

class Asignatura(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

class Docente(models.Model):
    nombre = models.CharField(max_length=50)

class Curso(models.Model):
    grupo = models.IntegerField()
    ranking = models.IntegerField()
    notapromedio = models.DecimalField(max_digits=3, decimal_places=2)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo_electronico = models.EmailField()
    curso = models.ManyToManyField(Curso)

class Comentario(models.Model):
    ususario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    comentario = models.CharField()



