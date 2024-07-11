from django import forms
from .models import Usuarios, Libros, Resenas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['nombre', 'email', 'password', 'tipo_usuario']
    

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libros
        fields = ['titulo', 'descripcion', 'imagen', 'calificacion', 'genero', 'autor']
        exclude = ['anio_publicacion']

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resenas
        fields = ['calificacion', 'comentario', 'fecha_resena']
        exclude = ['fecha_resena']
        
class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    email = forms.EmailField(label="Correo")
    mensaje = forms.CharField(max_length=500, label="Mensaje")
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']