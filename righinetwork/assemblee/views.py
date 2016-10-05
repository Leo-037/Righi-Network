import datetime
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect

from .models import *


# CREATE

@login_required(login_url = '/login/')
def create_assemblea_view(request):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		title = "Crea Assemblea"
		if request.method == "GET":
			form = AssembleaForm(initial = {'n_turni': 0})
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = AssembleaForm(request.POST)
			if form.is_valid():
				n_turni = form.cleaned_data['n_turni']
				assemblea = form.save()
				if n_turni >= 1:
					return HttpResponseRedirect(
						"/assemblee/aggiungi_turno/" + str(assemblea.id) + "/" + str(n_turni) + "/")
				else:
					return HttpResponseRedirect("/assemblee/" + str(assemblea.id) + "/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def create_turno_view(request, id_assemblea, n_turni):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		next = request.GET.get('next')
		if next:
			return redirect(next)
		title = "Aggiungi Turno"
		if request.method == "GET":
			assemblea = Assemblea.objects.get(id = id_assemblea)
			form = TurnoForm(initial = {'assemblea': assemblea})
			form.fields['assemblea'].widget = forms.HiddenInput()
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = TurnoForm(request.POST)
			form.save()

			assemblea = Assemblea.objects.get(id = id_assemblea)
			int(n_turni)
			if int(n_turni) > 1:
				return HttpResponseRedirect(
					"/assemblee/aggiungi_turno/" + str(assemblea.id) + "/" + str(n_turni - 1) + "/")
			else:
				return HttpResponseRedirect("/assemblee/" + str(assemblea.id) + "/")
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
			assemblea = Assemblea.objects.get(id = turno.assemblea.id)
			return HttpResponseRedirect("/assemblee/" + str(assemblea.id) + "/" + str(turno.id) + "/")
	else:
		raise Http404


# RETRIEVE

@login_required(login_url = '/login/')
def assemblee_view(request):
	title = "Assemblee"
	today = time.strftime("%Y-%m-%d")
	assemblee_correnti = Assemblea.objects.filter(mostra_assemblea__lte = today,
	                                              nascondi_assemblea__gt = today).order_by("-data_assemblea", "-id")
	assemblee_vecchie = Assemblea.objects.filter(mostra_assemblea__lte = today,
	                                             nascondi_assemblea__lte = today).order_by("-data_assemblea")
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
	if assemblea.mostra_assemblea < today < assemblea.nascondi_assemblea or assemblea.data_assemblea >= today - 1:
		mostra_iscrizione = False
	else:
		mostra_iscrizione = True

	title = "Turno delle " + str(turno.ora)

	context = {'turno': turno,
	           'gruppi': gruppi,
	           'gruppo_iscritto': gruppo_iscritto,
	           'mostra_iscrizione': mostra_iscrizione,
	           'title': title,
	           'recuperi': "false"
	           }

	return render(request, 'dettagli_turno.html', context)


# UPDATE

@login_required(login_url = '/login/')
def update_assemblea_view(request, id_assemblea):
	if not request.user.studente.is_rappr_istituto and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Assemblea, id = id_assemblea)
	form = AssembleaForm(request.POST or None, request.FILES or None, instance = instance, initial = {'n_turni': 0})
	form.fields['n_turni'].widget = forms.HiddenInput()
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "<h4><a href='#'>Assemblea</a> salvata</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/assemblee/" + str(instance.id) + "/")

	context = {
		"title": "Modifica assemblea",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


@login_required(login_url = '/login/')
def update_turno_view(request, id_turno):
	if not request.user.studente.is_rappr_istituto and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Turno, id = id_turno)
	form = TurnoForm(request.POST or None, request.FILES or None, instance = instance,
	                 initial = {'assemblea': instance.assemblea})
	form.fields['assemblea'].widget = forms.HiddenInput()
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "<h4><a href='#'>Turno</a> salvato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/assemblee/" + str(instance.assemblea.id) + "/" + str(instance.id) + "/")

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
			"/assemblee/" + str(instance.turno.assemblea.id) + "/" + str(instance.turno.id) + "/")

	context = {
		"title": "Modifica turno",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


# DELETE

@login_required(login_url = '/login/')
def delete_assemblea_view(request, id_assemblea):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		assemblea = Assemblea.objects.get(id = id_assemblea)
		assemblea.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/assemblee/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def delete_turno_view(request, id_turno):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		turno = Turno.objects.get(id = id_turno)
		turno.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/assemblee/" + str(turno.assemblea.id) + "/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def delete_gruppo_view(request, id_gruppo):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		gruppo = Gruppo.objects.get(id = id_gruppo)
		gruppo.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/assemblee/" + str(gruppo.turno.assemblea.id) + "/" + str(gruppo.turno.id) + "/")
	else:
		raise Http404


# ISCRITTI

@login_required(login_url = '/login/')
def iscritti_view(request, id_gruppo):
	title = "Iscritti al gruppo"
	gruppo = Gruppo.objects.get(pk = id_gruppo)
	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__cognome")

	return render(request, 'iscritti.html', {'title': title, 'gruppo': gruppo, 'iscritti': iscritti})


@login_required(login_url = '/login/')
def iscrizione_view(request, id_assemblea, id_turno, id_gruppo):
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
