import datetime
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .models import *


@login_required(login_url = '/login/')
def settimana_view(request):
	title = "Settimana dei recuperi"
	today = time.strftime("%Y-%m-%d")
	settimana = Settimana.objects.get(mostra_settimana__lte = today,
	                                  nascondi_settimana__gt = today)
	giorni = Giorno.objects.filter(settimana = settimana).order_by('data')
	context = {'settimana': settimana,
	           'giorni': giorni,
	           'title': title}
	return render(request, 'recuperi.html', context)


@login_required(login_url = '/login/')
def scegli_gruppo_view(request, id_turno):
	turno = Turno.objects.get(pk = id_turno)
	gruppi = Gruppo.objects.filter(turno = turno)
	gruppo_iscritto = None

	for gruppo in gruppi:
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
			gruppo_iscritto = gruppo

	today = datetime.date.today()
	settimana = turno.giorno.settimana
	if settimana.mostra_settimana < today and settimana.nascondi_settimana > today:
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


@login_required(login_url = '/login/')
def create_settimana_view(request):
	# if request.user.studente.is_rappr_istituto or request.user.is_superuser:
	# 	print(request.user.email)
	# 	title = "Crea Assemblea"
	# 	if request.method == "GET":
	# 		form = AssembleaForm()
	# 		return render(request, 'crea_assemblea.html', {'title': title, 'form': form})
	# 	elif request.method == "POST":
	# 		form = AssembleaForm(request.POST)
	# 		form.save()
	# 		return HttpResponseRedirect("/assemblee/")
	# else:
	raise Http404


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


@login_required(login_url = '/login/')
def iscritti_view(request, id_gruppo):
	title = "Iscritti al gruppo"
	gruppo = Gruppo.objects.get(pk = id_gruppo)
	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__cognome")

	return render(request, 'iscritti.html', {'title': title, 'gruppo': gruppo, 'iscritti': iscritti, 'recuperi': "true"})
