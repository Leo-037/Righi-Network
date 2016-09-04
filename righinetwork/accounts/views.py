from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from .forms import UserLoginForm, UserRegisterForm
from .models import Studente


User = get_user_model()

def login_view(request):
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')
		user = authenticate(username = username, password = password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/")
	return render(request, "authentication_form.html", {"form": form, "title": title})


def register_view(request):
	next = request.GET.get('next')
	title = "Registrati"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit = False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)

		nome = form.cleaned_data['nome']
		cognome = form.cleaned_data['cognome']
		classe = form.cleaned_data['classe']
		sezione = form.cleaned_data['sezione']

		studente = Studente(user = new_user, nome = nome, cognome = cognome, classe = classe, sezione = sezione)
		studente.save()

		if next:
			return redirect(next)
		return redirect("/")

	context = {
		"form": form,
		"title": title
	}
	return render(request, "authentication_form.html", context)


def logout_view(request):
	logout(request)
	return redirect("/login/")


@login_required(login_url = '/login/')
def cambia_password(request):
	raise Http404
	# studente = get_object_or_404(User, id = request.user.id)
	# form = UserRegisterForm(request.POST or None, request.FILES or None, instance = request.user.studente, initial = {'username': request.user.username, 'email': request.user.email}) #, request.FILES or None, instance = instance)
	# if form.is_valid():
	# 	studente = form.save(commit = False)
	# 	studente.save()
	# 	studente.success(request, "Impostazioni salvate", extra_tags = 'html_safe')
	# 	return HttpResponseRedirect(studente.get_absolute_url())
	#
	# context = {
	# 	"title": "Aggiorna",
	# 	"form": form,
	# }
	# return render(request, "authentication_form.html", context)
