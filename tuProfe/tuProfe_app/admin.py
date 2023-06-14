from django.contrib import admin
from .models import Docente, Autorizacion, Materia, Calificacion, Comentario

# Register your models here.

admin.site.register(Docente)
admin.site.register(Autorizacion)
admin.site.register(Materia)
admin.site.register(Calificacion)
admin.site.register(Comentario)

