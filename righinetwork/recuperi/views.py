import datetime
import time
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

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
	if not request.user.studente.is_attivato:
		raise Http404
	barare = False
	title = "Settimana dei recuperi"
	today = time.strftime("%Y-%m-%d")
	if request.user.is_superuser or request.user.studente.is_rappr_istituto:

		settimane = Settimana.objects.filter().order_by("-data_inizio")
	else:
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

	if barare and not (request.user.is_superuser or request.user.studente.is_rappr_istituto):
		settimana = []
		giorni = False
		tabella = False

	context = {'settimana': settimana,
	           'giorni': giorni,
	           'tabella': tabella,
	           'title': title}
	return render(request, 'recuperi.html', context)


@login_required(login_url = '/login/')
def dettagligiorno_view(request, id_giorno):
	if not request.user.studente.is_attivato:
		raise Http404
	giorno = Giorno.objects.get(pk = id_giorno)
	turni = Turno.objects.filter(giorno = giorno).order_by("ora")
	context = {'giorno': giorno,
	           'turni': turni,
	           }
	return render(request, 'dettagli_giorno.html', context)


@login_required(login_url = '/login/')
def dettagliturno_view(request, id_turno):
	if not request.user.studente.is_attivato:
		raise Http404
	barare = True

	turno = Turno.objects.get(pk = id_turno)
	if request.user.is_superuser or request.user.studente.is_rappr_istituto:
		gruppi = Gruppo.objects.filter(turno = turno).order_by('recupero', 'sede')
	else:
		if request.user.studente.classe == 1 or request.user.studente.classe == 2:
			gruppi = Gruppo.objects.filter(turno = turno, sede = "Succursale").order_by('-recupero')
		elif request.user.studente.classe == 3 or request.user.studente.classe == 4 or request.user.studente.classe == 5:
			gruppi = Gruppo.objects.filter(turno = turno, sede = "Sede").order_by('-recupero')
	gruppo_iscritto = None

	for gruppo in gruppi:
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
			gruppo_iscritto = gruppo
			break

	# Filtro gruppi
	query = request.GET.get("q")
	if query:
		gruppi = gruppi.filter(
			Q(titolo__icontains = query) |
			Q(sede__icontains = query) |
			Q(descrizione__icontains = query) |
			Q(aula__icontains = query) |
			Q(host__icontains = query)
		).distinct()

	today = datetime.date.today()
	settimana = turno.giorno.settimana
	if settimana.mostra_settimana < today < settimana.nascondi_settimana:
		mostra_iscrizione = False
	else:
		mostra_iscrizione = True

	title = "Turno delle " + str(turno.ora)

	studenti = Studente.objects.all().order_by('classe', 'sezione', 'cognome', 'nome')

	if request.method == "POST":
		for gruppo in Gruppo.objects.filter(recupero = True, turno = turno):
			nome_form = 'iscritti-' + str(gruppo.id)
			da_iscrivere = request.POST.getlist(nome_form)
			for id in da_iscrivere:
				studente = Studente.objects.filter(pk = id)[0]
				if gruppo.iscritti == gruppo.iscritti_massimi:
					break
				if len(Iscritto.objects.filter(studente = studente, gruppo__turno = gruppo.turno)) == 0:
					iscritto = Iscritto(studente = studente, gruppo = gruppo)
					gruppo.iscritti += 1
					iscritto.save()
					gruppo.save()
		return redirect("/recuperi/scegli_gruppo/" + str(turno.id) + "/")

	context = {'studenti': studenti,
	           'turno': turno,
	           'gruppi': gruppi,
	           'gruppo_iscritto': gruppo_iscritto,
	           'mostra_iscrizione': mostra_iscrizione,
	           'title': title,
	           'recuperi': "true",
	           'barare': barare,
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
		"title": "Modifica gruppo",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


# DELETE

@login_required(login_url = '/login/')
def delete_settimana_view(request, id_settimana):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		settimana = Settimana.objects.get(id = id_settimana)
		settimana.delete()
		messages.success(request, "<h4>Cancellata</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/recuperi/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def delete_turno_view(request, id_turno):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		turno = Turno.objects.get(id = id_turno)
		id_giorno = turno.giorno.id
		turno.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/recuperi/" + str(id_giorno) + "/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def delete_gruppo_view(request, id_gruppo):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		gruppo = Gruppo.objects.get(id = id_gruppo)
		id_turno = gruppo.turno.id
		gruppo.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/recuperi/scegli_gruppo/" + str(id_turno) + "/")
	else:
		raise Http404


# ISCRITTI


@login_required(login_url = '/login/')
def iscritti_view(request, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404
	title = "Iscritti al gruppo"
	gruppo = Gruppo.objects.get(pk = id_gruppo)
	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__cognome")

	if request.method == "POST":
		da_iscrivere = request.POST.getlist('iscritto_da_cancellare')
		for id in da_iscrivere:
			iscritto = Iscritto.objects.get(pk = id)
			gruppo.iscritti -= 1
			iscritto.delete()
			gruppo.save()
			if gruppo.iscritti == 0:
				return redirect("/recuperi/scegli_gruppo/" + str(gruppo.turno.id) + "/")

	return render(request, 'iscritti.html',
	              {'title': title, 'gruppo': gruppo, 'iscritti': iscritti, 'recuperi': "true"})


@login_required(login_url = '/login/')
def pdf_iscritti_view(request, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404
	gruppo = Gruppo.objects.get(pk = id_gruppo)
	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'attachment; filename="' + gruppo.titolo + '".pdf"'

	buffer = BytesIO()

	doc = SimpleDocTemplate(buffer, rightMargin = 35,
	                        leftMargin = 35, topMargin = 35, bottomMargin = 18)
	doc.pagesize = portrait(A4)

	# TABELLA

	elements = []

	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__cognome")
	data = [
		["#", "Cognome", "Nome", "Classe", "Sezione", "A o P"]
	]

	i = 1
	for iscritto in iscritti:
		row = [str(i), iscritto.studente.cognome, iscritto.studente.nome, str(iscritto.studente.classe),
		       iscritto.studente.sezione, ""]
		data.append(row)
		i += 1

	style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
	                    ('TEXTCOLOR', (1, 1), (-2, -2), colors.black),
	                    ('VALIGN', (0, 0), (0, -1), 'TOP'),
	                    ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
	                    ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
	                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
	                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
	                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
	                    ])

	s = getSampleStyleSheet()
	s = s["BodyText"]
	s.wordWrap = 'LTR'
	data2 = [[Paragraph(cell, s) for cell in row] for row in data]
	t = Table(data2)
	t.setStyle(style)

	# TITOLO

	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name = 'Custom', fontSize = 19, alignment = 1, wordWrap = 'CJK', leading = 25))

	titolo = Paragraph(gruppo.titolo + " - Turno delle " + str(gruppo.turno.ora) + " di " + gruppo.turno.giorno.nome,
	                   styles['Custom'])

	elements.append(titolo)
	elements.append(Spacer(1, 0.5 * cm))
	elements.append(t)
	doc.build(elements)

	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)

	return response


@login_required(login_url = '/login/')
def iscrizione_view(request, id_settimana, id_giorno, id_turno, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.method == "POST":
		turno = Turno.objects.filter(id = id_turno)
		for gruppo in Gruppo.objects.filter(turno = turno):
			if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
				Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo).delete()
				gruppo.iscritti -= 1
				gruppo.save()

		gruppo = Gruppo.objects.get(pk = id_gruppo)
		if gruppo.iscritti != gruppo.iscritti_massimi:
			iscritto = Iscritto(studente = request.user.studente, gruppo = gruppo)
			gruppo.iscritti += 1
			iscritto.save()
			gruppo.save()

			return HttpResponseRedirect("/recuperi/scegli_gruppo/" + str(id_turno) + "/")
		else:
			raise Http404


@login_required(login_url = '/login/')
def disiscrizione_view(request, id_settimana, id_giorno, id_turno, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.method == "POST":
		gruppo = Gruppo.objects.get(pk = id_gruppo)
		iscritto = Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo)
		gruppo.iscritti -= 1
		iscritto.delete()
		gruppo.save()

		return HttpResponseRedirect("/recuperi/scegli_gruppo/" + str(id_turno) + "/")
