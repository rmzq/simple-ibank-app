from django.shortcuts import render, redirect
from .forms import NasabahRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
# Create your views here.

def daftar(request):
	if request.method == 'POST':
		form = NasabahRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Akun sudah dibuat untuk {username}!, silahkan masuk')
			return redirect('masuk')
	else:
		form = NasabahRegisterForm()
	return render (request, 'autentikasi/daftar.html', {'form':form})

@login_required
def profil(request):
	return render(request, 'autentikasi/profil.html',{})

# def masuk(request):
# 	form = views.LoginView(AutheticationForm)
# 	print(form)
# 	return render(request, 'autentikasi/masuk.html', {})

