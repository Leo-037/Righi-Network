import random

from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

)
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, Http404

from .forms import UserLoginForm, StudenteRegisterForm, CambiaPasswordForm, ClasseForm, MailForm
from .models import Studente

User = get_user_model()


@login_required(login_url = '/login/')
def classi_view(request):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		studenti = Studente.objects.all()

		classi = [1, 2, 3, 4, 5]
		sezioni = []

		classi_complete = []

		for studente in studenti:
			sezione = studente.sezione
			if sezione not in sezioni:
				sezioni.append(sezione)
				sezioni.sort()

		for classe in classi:
			for sezione in sezioni:
				if len(Studente.objects.filter(classe = classe, sezione = sezione)) > 0:
					classe_completa = (classe, sezione)
					classi_complete.append(classe_completa)

		if request.method == "GET":
			form = ClasseForm()
			studenti_totali = len(Studente.objects.all())
			studenti_attivati = len(Studente.objects.filter(is_attivato = True))
			return render(request, "classi.html", {'form': form, 'classi': classi_complete, 'studenti_attivati': studenti_attivati, 'studenti_totali': studenti_totali})
		elif request.method == "POST":
			form = ClasseForm(request.POST)
			if form.is_valid():
				classe = form.cleaned_data['classe']
				sezione = form.cleaned_data['sezione']
				sezione = sezione.upper()

				classesezione = str(classe) + "-" + str(sezione)

				return redirect("/gestione/" + classesezione + "/")

	else:
		raise Http404


@login_required(login_url = '/login/')
def dettagli_classe_view(request, classesezione):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:

		classe, sezione = classesezione.split('-')
		studenti_attivi = Studente.objects.filter(classe = classe, sezione = sezione, is_attivato = True).order_by(
			"cognome", "nome")
		studenti_inattivi = Studente.objects.filter(classe = classe, sezione = sezione, is_attivato = False).order_by(
			"cognome", "nome")

		if request.method == "GET":
			form = StudenteRegisterForm(
				initial = {'username': "Temp", 'password': 'PASSWORD1', 'classe': classe, 'sezione': sezione})
			form.fields['password'].widget = forms.HiddenInput()
			form.fields['username'].widget = forms.HiddenInput()
			form.fields['classe'].widget = forms.HiddenInput()
			form.fields['sezione'].widget = forms.HiddenInput()
			return render(request, 'dettagli_classe.html',
			              {'form': form, 'classe': classe, 'sezione': sezione, 'studenti_attivi': studenti_attivi,
			               'studenti_inattivi': studenti_inattivi})
		elif request.method == "POST":
			form = StudenteRegisterForm(request.POST)
			if form.is_valid():
				user = form.save(commit = False)
				password = generate_password(8)
				user.set_password(password)

				nome = form.cleaned_data['nome']
				cognome = form.cleaned_data['cognome']
				classe = form.cleaned_data['classe']
				sezione = form.cleaned_data['sezione']

				user.username = clean_username(nome, cognome)
				user.save()

				new_user = authenticate(username = user.username, password = password)

				studente = Studente(user = new_user, nome = nome, cognome = cognome, classe = classe, sezione = sezione,
				                    password = password)
				studente.save()

			return redirect("/gestione/" + classesezione + "/")
	else:
		raise Http404


def clean_username(nome, cognome):
	newusername = nome + "_" + cognome
	newusername = newusername.lower()
	newusername = newusername.replace(" ", "_")
	newusername = newusername.replace("à", "a")
	newusername = newusername.replace("è", "e")
	newusername = newusername.replace("ì", "i")
	newusername = newusername.replace("ò", "o")
	newusername = newusername.replace("ù", "u")
	while len(User.objects.filter(username = newusername)) != 0:
		pezzi = newusername.split("_")
		numero = pezzi[-1]
		if numero.isdigit():
			del pezzi[-1]

			numero = int(numero) + 1
			pezzi.append(numero)
			newusername = ""
			for pezzo in pezzi:
				newusername += str(pezzo) + "_"
			newusername = newusername[:-1]
		else:
			newusername += "_1"

	return newusername


def generate_password(length):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	upperalphabet = alphabet.upper()
	pw_len = length
	pwlist = []

	for i in range(pw_len // 3):
		pwlist.append(alphabet[random.randrange(len(alphabet))])
		pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
		pwlist.append(str(random.randrange(10)))
	for i in range(pw_len - len(pwlist)):
		pwlist.append(alphabet[random.randrange(len(alphabet))])

	random.shuffle(pwlist)
	pwstring = "".join(pwlist)

	return pwstring


def login_view(request):
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')
		user = authenticate(username = username, password = password)
		login(request, user)
		if user.studente.is_attivato:
			if next:
				return redirect(next)
			return redirect("/")
		else:
			return redirect("/gestione/aggiorna/email/")

	return render(request, "authentication_form.html", {"form": form, "title": title})


@login_required(login_url = '/login/')
def aggiorna_mail_view(request):
	form = MailForm(request.POST or None)
	if form.is_valid():
		codice = generate_password(6)
		indirizzo = form.cleaned_data.get('email')
		send_mail('Codice di verifica RighiNetwork',
		          """Il tuo codice per confermare l'indirizzo email inserito nel RighiNetwork è: \n{0}.\nQuesto codice è valido una sola volta, e serve solo per confermare l'indirizzo email.""".format(
			          codice), 'RighiNetwork <noreply@righi-network.com>',
		          [indirizzo])
		request.session['codice_mail'] = codice
		request.session['email'] = indirizzo
		return redirect("/gestione/aggiorna/password")

	context = {
		"form": form,
		"title": "Aggiungi Email"
	}
	return render(request, "crispy_form.html", context)


@login_required(login_url = '/login/')
def aggiorna_password_view(request):
	title = "Aggiorna Account"
	form = CambiaPasswordForm(request.POST or None, request = request)
	if form.is_valid():
		user = User.objects.get(username__exact = request.user.username)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.email = request.session.get('email')
		user.save()
		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)
		studente = Studente.objects.get(user = user)
		studente.is_attivato = True
		studente.password = ""
		studente.save()

		return redirect("/")

	context = {
		"form": form,
		"link": '<a href="/gestione/aggiorna/email/">Modifica Indirizzo Email</a>',
		"title": title
	}
	return render(request, "crispy_form.html", context)


def logout_view(request):
	logout(request)
	return redirect("/login/")


@login_required(login_url = '/login/')
def elimina_studente_view(request, username):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		studente = User.objects.get(username = username)
		studente.delete()
		url = request.get_full_path()[:14]
		return redirect(url)
	else:
		raise Http404

@login_required(login_url = '/login/')
def cambia_password(request):
	if not request.user.studente.is_attivato:
		raise Http404
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
