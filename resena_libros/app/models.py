from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.
class Usuarios(models.Model):
    TIPO_USUARIO = (
        ('admin', 'Administrador'),
        ('lector', 'Lector'),
    )
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=20, blank=False, null=False)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, default='lector', blank=False, null=False)


class Autores(models.Model):
    nombre = models.CharField(max_length=200, blank=False, null=False)
    seguidor = models.ManyToManyField(Usuarios, related_name='autores_favoritos', blank=True)

    def __str__(self):
        return self.nombre

    def notificar_seguidores(self, libro):
        for seguidor in self.seguidores.all():
            print(f"Notificación enviada a {seguidor.nombre} sobre el nuevo libro: {libro.titulo}")
        

class Generos(models.Model):
    nombre = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.nombre
       
    
class Libros(models.Model):
    titulo = models.CharField(max_length=300, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    anio_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes_libros/', blank=False, null=False)
    calificacion = models.FloatField(default=0.0)
    genero = models.ForeignKey(Generos, on_delete=models.PROTECT, null=True, blank=True)
    autor = models.ForeignKey(Autores, on_delete=models.CASCADE, blank=False, null=False)
    

    def __str__(self):
        return self.titulo
    
    def actualizar_calificacion(self):
        resenas = self.resena_set.all()
        total_calificaciones = resenas.count()
        if total_calificaciones > 0:
            suma_calificaciones = sum(resena.calificacion for resena in resenas)
            self.calificacion = suma_calificaciones / total_calificaciones
        else:
            self.calificacion = 0.0
        self.save()
        
    def notificar_nuevo_libro(sender, instance, created, **kwargs):
        if created:
            instance.autor.notificar_seguidores(instance)
        
    
class Resenas(models.Model):
    libro = models.ForeignKey(Libros, on_delete=models.CASCADE, blank=False, null=False)
    nombre = models.ForeignKey(Usuarios, on_delete=models.CASCADE, blank=False, null=False)
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField()
    fecha_resena = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre.nombre} - {self.libro.titulo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.libro.actualizar_calificacion()
    
    
class Contactos(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre   