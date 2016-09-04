import datetime
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .models import *


@login_required(login_url = '/login/')
def assemblee_view(request):
	title = "Assemblee"
	today = time.strftime("%Y-%m-%d")
	assemblee_correnti = Assemblea.objects.filter(mostra_assemblea__lte = today,
	                                              nascondi_assemblea__gt = today).order_by("-data_assemblea", "-id")
	assemblee_vecchie = Assemblea.objects.filter(mostra_assemblea__lte = today, nascondi_assemblea__lte = today).order_by("-data_assemblea")
	assemblee_future = Assemblea.objects.filter(mostra_assemblea__gte = today).order_by("data_assemblea")
	context = {'assemblee_correnti': assemblee_correnti,
	           'assemblee_future': assemblee_future,
	           'assemblee_vecchie': assemblee_vecchie,
	           'title': title}
	return render(request, 'assemblee.html', context)


@login_required(login_url = '/login/')
def dettagliassemblea_view(request, id_assemblea):
	assemblea = Assemblea.objects.get(pk = id_assemblea)
	turni = Turno.objects.filter(assemblea = assemblea).order_by("ora")
	context = {'assemblea': assemblea,
	           'turni': turni,
	           }
	return render(request, 'dettagli_assemblea.html', context)


@login_required(login_url = '/login/')
def dettagliturno_view(request, id_turno):
	turno = Turno.objects.get(pk = id_turno)
	gruppi = Gruppo.objects.filter(turno = turno)
	gruppo_iscritto = None

	for gruppo in gruppi:
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
			gruppo_iscritto = gruppo

	today = datetime.date.today()
	assemblea = turno.assemblea
	if assemblea.mostra_assemblea < today and assemblea.nascondi_assemblea > today:
		mostra_iscrizione = False
	else:
		mostra_iscrizione = True

	title = "Turno delle " + str(turno.ora)

	context = {'turno': turno,
	           'gruppi': gruppi,
	           'gruppo_iscritto': gruppo_iscritto,
	           'mostra_iscrizione': mostra_iscrizione,
	           'title': title,
	           }

	print(request.user.studente.nome)

	return render(request, 'dettagli_turno.html', context)


@login_required(login_url = '/login/')
def create_assemblea_view(request):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		print(request.user.email)
		title = "Crea Assemblea"
		if request.method == "GET":
			form = AssembleaForm()
			return render(request, 'crea_assemblea.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = AssembleaForm(request.POST)
			form.save()
			return HttpResponseRedirect("/assemblee/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def iscrizione_view(request, id_assemblea, id_turno, id_gruppo):
	if request.method == "POST":
		for gruppo in Gruppo.objects.all():
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

			return HttpResponseRedirect("/assemblee/" + str(id_assemblea) + "/" + str(id_turno) + "/")
		else:
			raise Http404


@login_required(login_url = '/login/')
def disiscrizione_view(request, id_assemblea, id_turno, id_gruppo):
	if request.method == "POST":
		gruppo = Gruppo.objects.get(pk = id_gruppo)
		iscritto = Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo)
		gruppo.iscritti -= 1
		iscritto.delete()
		gruppo.save()

		return HttpResponseRedirect("/assemblee/" + str(id_assemblea) + "/" + str(id_turno) + "/")


@login_required(login_url = '/login/')
def iscritti_view(request, id_gruppo):
	title = "Iscritti al gruppo"
	gruppo = Gruppo.objects.get(pk = id_gruppo)
	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione", "studente__cognome")

	return render(request, 'iscritti.html', {'title': title, 'gruppo': gruppo, 'iscritti': iscritti})
