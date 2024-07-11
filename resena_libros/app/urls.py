#urls app
from django.urls import path
from app.views import inicio, contacto, exito, salir, entrar, register, crear_libro, listar_libros, ver_resena, crear_resena

urlpatterns = [
    path('', inicio, name='inicio'),
    path('contacto/', contacto, name="contacto"),
    path('exito/', exito, name="exito"),
    path('login/', entrar, name="entrar"),
    path('logout/', salir, name="salir"),
    path('register/', register, name="register"),
    path('libro/nuevo/', crear_libro, name='crear_libro'),
    path('libros/', listar_libros, name='listar_libros'),
    path('libro/<int:id>/resena/', ver_resena, name='ver_resena'),
    path('libro/resena/crear', crear_resena, name='crear_resena')
]