from django.urls import path
from .views import index, duenos, detalle_dueno, vacunas
from web.views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'), #as_view() es necesario para convertir la clase en una vista que pueda ser llamada por Django
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'), #CustomLogoutView es una clase que hereda de LogoutView, y se encarga de cerrar la sesión del usuario y redirigirlo a la página de login, además de mostrar un mensaje de éxito al cerrar sesión.
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('owners/', duenos, name="duenos"),
    path('owners/<int:dueno_id>/', detalle_dueno, name="detalle_dueno"),
    path('vacunas/', vacunas, name="vacunas"),
]
