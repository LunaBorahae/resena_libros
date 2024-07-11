from django.contrib import admin
from app.models import Contactos

# Register your models here.
@admin.register(Contactos)
class ContactosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'mensaje')