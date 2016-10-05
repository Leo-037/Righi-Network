import datetime
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect

from .models import *


# CREATE


@login_required(login_url = '/login/')
def create_settimana_view(request):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		title = "Crea Settimana"
		if request.method == "GET":
			form = SettimanaForm()
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = SettimanaForm(request.POST)
			if form.is_valid():
				settimana = form.save()
				primo_giorno = settimana.data_inizio
				ultimo_giorno = settimana.data_fine
				numero_giorni = abs((primo_giorno - ultimo_giorno).days) + 1
				print(str(numero_giorni))

				giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
				for data in (primo_giorno + datetime.timedelta(n) for n in range(numero_giorni)):
					g = Giorno(data = data, nome = giorni[data.weekday()], settimana = settimana)
					g.save()

				return HttpResponseRedirect("/recuperi/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def create_turno_view(request, id_giorno):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		next = request.GET.get('next')
		if next:
			return redirect(next)
		title = "Aggiungi Turno"
		if request.method == "GET":
			giorno = Giorno.objects.get(id = id_giorno)
			form = TurnoForm(initial = {'giorno': giorno})
			form.fields['giorno'].widget = forms.HiddenInput()
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = TurnoForm(request.POST)
			form.save()

			giorno = Giorno.objects.get(id = id_giorno)
			return HttpResponseRedirect("/recuperi/" + str(giorno.id) + "/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def create_gruppo_view(request, id_turno):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		next = request.GET.get('next')
		if next:
			return redirect(next)
		title = "Aggiungi Gruppo"
		if request.method == "GET":
			turno = Turno.objects.get(id = id_turno)
			form = GruppoForm(initial = {'turno': turno})
			form.fields['turno'].widget = forms.HiddenInput()
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = GruppoForm(request.POST)
			form.save()

			turno = Turno.objects.get(id = id_turno)
			return HttpResponseRedirect("/recuperi/scegli_gruppo/" + str(turno.id) + "/")
	else:
		raise Http404


# RETRIEVE


@login_required(login_url = '/login/')
def settimana_view(request):
	title = "Settimana dei recuperi"
	today = time.strftime("%Y-%m-%d")
	settimane = Settimana.objects.filter(mostra_settimana__lte = today,
	                                     nascondi_settimana__gt = today).order_by("-data_inizio")
	if len(settimane) > 0:
		settimana = settimane[0]
		giorni = Giorno.objects.filter(settimana = settimana).order_by('data')

		temp = []
		for giorno in giorni.annotate(num_turni = Count('turno')):
			temp.append(giorno.num_turni)

		numero_turni = max(temp)

		tabella = []

		for index in range(0, numero_turni):
			riga = []
			for giorno in giorni:

				turni = Turno.objects.filter(giorno = giorno).order_by('ora')

				if index < len(turni):
					turno = turni[index]
					gruppi = Gruppo.objects.filter(turno = turno)
					if len(gruppi) > 0:
						for gruppo in gruppi:
							iscritti = Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo)
							if len(iscritti) > 0:
								riga.append(gruppo)
								break
						else:
							riga.append(turno.id)
					else:
						riga.append(0)
				else:
					riga.append(0)

			tabella.append(riga)

	else:
		settimana = []
		giorni = False
		tabella = False

	print(tabella)
	context = {'settimana': settimana,
	           'giorni': giorni,
	           'tabella': tabella,
	           'title': title}
	return render(request, 'recuperi.html', context)


@login_required(login_url = '/login/')
def dettagligiorno_view(request, id_giorno):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		giorno = Giorno.objects.get(pk = id_giorno)
		turni = Turno.objects.filter(giorno = giorno).order_by("ora")
		context = {'giorno': giorno,
		           'turni': turni,
		           }
		return render(request, 'dettagli_giorno.html', context)
	else:
		raise Http404


@login_required(login_url = '/login/')
def dettagliturno_view(request, id_turno):
	turno = Turno.objects.get(pk = id_turno)
	if request.user.studente.classe == 1 or request.user.studente.classe == 2:
		gruppi = Gruppo.objects.filter(turno = turno, sede = "Succursale").order_by('recupero')
	elif request.user.studente.classe == 3 or request.user.studente.classe == 4 or request.user.studente.classe == 5:
		gruppi = Gruppo.objects.filter(turno = turno, sede = "Sede").order_by('recupero')
	gruppo_iscritto = None

	for gruppo in gruppi:
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
			gruppo_iscritto = gruppo
			break

	today = datetime.date.today()
	settimana = turno.giorno.settimana
	if settimana.mostra_settimana < today < settimana.nascondi_settimana:
		mostra_iscrizione = False
	else:
		mostra_iscrizione = True

	title = "Turno delle " + str(turno.ora)

	context = {'turno': turno,
	           'gruppi': gruppi,
	           'gruppo_iscritto': gruppo_iscritto,
	           'mostra_iscrizione': mostra_iscrizione,
	           'title': title,
	           'recuperi': "true"
	           }

	return render(request, 'dettagli_turno.html', context)


# UPDATE


@login_required(login_url = '/login/')
def update_turno_view(request, id_turno):
	if not request.user.studente.is_rappr_istituto and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Turno, id = id_turno)
	form = TurnoForm(request.POST or None, request.FILES or None, instance = instance,
	                 initial = {'giorno': instance.giorno})
	form.fields['giorno'].widget = forms.HiddenInput()
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "<h4><a href='#'>Turno</a> salvato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/recuperi/scegli_gruppo/" + str(instance.id) + "/")

	context = {
		"title": "Modifica turno",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


@login_required(login_url = '/login/')
def update_gruppo_view(request, id_gruppo):
	if not request.user.studente.is_rappr_istituto and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Gruppo, id = id_gruppo)
	form = GruppoForm(request.POST or None, request.FILES or None, instance = instance,
	                  initial = {'turno': instance.turno})
	form.fields['turno'].widget = forms.HiddenInput()
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "<h4><a href='#'>Gruppo</a> salvato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect(
			"/recuperi/scegli_gruppo/" + str(instance.turno.id) + "/")

	context = {
		"title": "Modifica turno",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


# DELETE


# ISCRITTI


@login_required(login_url = '/login/')
def iscritti_view(request, id_gruppo):
	title = "Iscritti al gruppo"
	gruppo = Gruppo.objects.get(pk = id_gruppo)
	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__cognome")

	return render(request, 'iscritti.html',
	              {'title': title, 'gruppo': gruppo, 'iscritti': iscritti, 'recuperi': "true"})


@login_required(login_url = '/login/')
def iscrizione_view(request, id_settimana, id_giorno, id_turno, id_gruppo):
	if request.method == "POST":
		turno = Turno.objects.filter(id = id_turno)
		for gruppo in Gruppo.objects.filter(turno = turno):
			if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
				Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo).delete()
				gruppo.iscritti -= 1
				gruppo.save()

		gruppo = Gruppo.objects.get(pk = id_gruppo)
		if not gruppo.iscritti == gruppo.iscritti_massimi:
			iscritto = Iscritto(studente = request.user.studente, gruppo = gruppo)
			gruppo.iscritti += 1
			iscritto.save()
			gruppo.save()

			return HttpResponseRedirect("/recuperi/scegli_gruppo/" + str(id_turno) + "/")
		else:
			raise Http404


@login_required(login_url = '/login/')
def disiscrizione_view(request, id_settimana, id_giorno, id_turno, id_gruppo):
	if request.method == "POST":
		gruppo = Gruppo.objects.get(pk = id_gruppo)
		iscritto = Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo)
		gruppo.iscritti -= 1
		iscritto.delete()
		gruppo.save()

		return HttpResponseRedirect("/recuperi/scegli_gruppo/" + str(id_turno) + "/")
