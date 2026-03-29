from django.contrib import admin
from .models import *

# Register your models here.

#admin.site.register(Dueno)
admin.site.register(Vacuna)
#admin.site.register(Mascota)
admin.site.register(ExpedienteMedico)


@admin.register(Dueno)
class DuenoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono')
    search_fields = ('nombre', 'telefono')

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'especie', 'dueno')
    search_fields = ('nombre', 'especie', 'dueno__nombre') #dueno__nombre se utiliza para buscar por el nombre del dueño asociado a la mascota, lo que permite realizar búsquedas más completas y precisas en el panel de administración de Django.
    list_filter = ('especie', 'dueno') #list_filter se utiliza para agregar filtros en el panel de administración de Django, lo que permite filtrar las mascotas por especie y por dueño, facilitando la gestión y visualización de las mascotas en función de estos criterios.
    filter_horizontal = ('vacunas',) #filter_horizontal se utiliza para mostrar un widget de selección horizontal en el panel de administración de Django, lo que facilita la gestión de las relaciones muchos a muchos entre Mascota y Vacuna. Esto permite seleccionar y deseleccionar vacunas asociadas a una mascota de manera más intuitiva y eficiente.

