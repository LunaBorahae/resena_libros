from django.shortcuts import render, redirect, get_object_or_404
from app.models import Resenas, Libros, Usuarios, Contactos
from app.forms import UsuarioForm, LibroForm, ResenaForm, ContactoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.forms import CustomUserCreationForm
# Create your views here.

def inicio(request):
    return render(request, "indice.html", {})


def contacto(request):
    mensaje = None
    if request.method == "POST":
        contacto_form = ContactoForm(request.POST)
        if contacto_form.is_valid():
            Contactos.objects.create(**contacto_form.cleaned_data)
            return redirect("exito")
        else:
            mensaje = "Favor corregir errores en el formulario"
    else:
        contacto_form = ContactoForm()

    return render(request, "contact.html", {"form": contacto_form, "mensaje": mensaje})


def exito(request):
    return render(request, 'exito.html')


def entrar(request):
    if request.method == 'POST':
        user = authenticate(request.POST)
        if user is not None:
            login(request, user)
            return redirect('exito')
        else:
            return redirect('entrar')
    return render(request, "registration/login.html")


def salir(request):
    logout(request)
    return redirect("/")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            login(request, user)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/register.html", {"form": form})

#crud para usuarios

def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    return usuarios


def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return redirect('listar_usuarios')


def ver_usuario(request, usuario_id):
    usuario = Usuarios.objects.filter(pk=usuario_id).first()
    if usuario is None:
        return redirect('listar_usuarios')
    return redirect('listar_usuarios')


def actualizar_usuario(request, usuario_id):
    usuario = Usuarios.objects.filter(pk=usuario_id).first()
    if usuario is None:
        return redirect('listar_usuarios')
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('ver_usuario', usuario_id=usuario_id)
    else:
        form = UsuarioForm(instance=usuario)
    return redirect('listar_usuarios')


def eliminar_usuario(request, usuario_id):
    usuario = Usuarios.objects.filter(pk=usuario_id).first()
    if usuario is None:
        return redirect('listar_usuarios')
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return redirect('listar_usuarios')




#cruda para libros
def listar_libros(request):
    libros = Libros.objects.all()
    return render(request, 'ver_libro.html', {'libros': libros})
    

@login_required
def crear_libro(request):
    if request.method == 'POST':
        print(request.POST)
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = LibroForm()
    return render(request, 'crear_libro.html', {'form': form})



def ver_libro(request, libro_id):
    libro = Libros.objects.filter(pk=libro_id).first()
    if libro is None:
        return redirect('listar_libros')
    return render(request, 'ver_libro.html', {'libro': libro})


def actualizar_libro(request, libro_id):
    libro = Libros.objects.filter(pk=libro_id).first()
    if libro is None:
        return redirect('listar_libros')
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('ver_libro', libro_id=libro_id)
    else:
        form = LibroForm(instance=libro)
    return redirect('listar_libros')


def eliminar_libro(request, libro_id):
    libro = Libros.objects.filter(pk=libro_id).first()
    if libro is None:
        return redirect('listar_libros')
    if request.method == 'POST':
        libro.delete()
        return redirect('listar_libros')
    return redirect('listar_libros')



#crud para reseñas
def listar_resenas(request):
    resenas = Resenas.objects.all()
    return resenas


def crear_resena(request, id):
    libro = get_object_or_404(Libros, id=id)
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        print("estoy aki")
        print(dir(form))
        if form.is_valid():
            form.save()
            return redirect('listar_libros')
    else:
        form = ResenaForm()
    return render(request, 'crear_resena.html', {'resena_form': form})

def ver_resena(request, id):
    libro = get_object_or_404(Libros, id=id)
    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('listar_libros')
    else:
        form = ResenaForm(instance=libro)
    return render(request, 'resena.html', {'libro': libro, 'resena_form': form})

def actualizar_resena(request, resena_id):
    resena = Resenas.objects.filter(pk=resena_id).first()
    if resena is None:
        return redirect('listar_libros')
    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena)
        if form.is_valid():
            form.save()
            return redirect('ver_resena', resena_id=resena_id)
    else:
        form = ResenaForm(instance=resena)
    return redirect('listar_libros')


def eliminar_resena(request, resena_id):
    resena = Resenas.objects.filter(pk=resena_id).first()
    if resena is None:
        return redirect('listar_libros')
    if request.method == 'POST':
        resena.delete()
        return redirect('listar_libros')
    return redirect('listar_libros')
