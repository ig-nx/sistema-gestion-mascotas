from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import *

class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect(reverse('register'))

        if User.objects.filter(username=email).exists(): # Verificar si el correo electrónico ya está registrado en la base de datos. Si es así, se muestra un mensaje de error y se redirige al usuario a la página de registro para que pueda intentar con otro correo electrónico.
            messages.error(request, 'El correo electronico ya esta registrado')
            return redirect(reverse('register'))        
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )
        # user.is_active = False
        UserProfile.objects.create(user=user, tipo='cliente')
        user.save()
        user = authenticate(username=email, password=password1)
        if user is not None:
            login(request, user)
        messages.success(request, 'Usuario creado exitosamente')
        return redirect('index')


class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "Sesion Iniciada Exitosamente"
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.WARNING, "Sesion Cerrada Exitosamente")
        return response



@login_required
def index(request):
    mascotas = Mascota.objects.all().select_related('dueno', 'expediente').prefetch_related('vacunas')

    context = {
        'mascotas': mascotas,
    }
    return render(request, 'index.html', context)

def duenos(request):
    duenos = Dueno.objects.all().prefetch_related('mascotas')
    context = {
        'duenos': duenos,
    }
    return render(request, 'duenos.html', context)

def detalle_dueno(request, dueno_id):
    dueno = get_object_or_404(
        Dueno.objects.prefetch_related('mascotas'),
        id=dueno_id,
    )
    context = {
        'dueno': dueno,
    }
    return render(request, 'detalle_dueno.html', context)

def vacunas(request):
    vacunas = Vacuna.objects.exclude(nombre__iexact="Sin vacunas").prefetch_related('mascotas_vacunas')
    context = {
        'vacunas': vacunas,
    }
    return render(request, 'vacunas.html', context)
