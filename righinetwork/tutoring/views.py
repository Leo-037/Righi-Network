from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .models import *


# Create your views here.

@login_required(login_url = '/login/')
def list_tutors(request):
	if not request.user.studente.is_attivato:
		raise Http404
	title = "Tutoring"
	if request.user.studente.classe == 1:
		tutori_approvati = Tutor.objects.filter(approvato = True, prima = True).exclude(
			studente = request.user.studente)
	elif request.user.studente.classe == 2:
		tutori_approvati = Tutor.objects.filter(approvato = True, seconda = True).exclude(
			studente = request.user.studente)
	elif request.user.studente.classe == 3:
		tutori_approvati = Tutor.objects.filter(approvato = True, terza = True).exclude(
			studente = request.user.studente)
	elif request.user.studente.classe == 4:
		tutori_approvati = Tutor.objects.filter(approvato = True, quarta = True).exclude(
			studente = request.user.studente)
	else:
		tutori_approvati = Tutor.objects.filter(approvato = True, quinta = True).exclude(
			studente = request.user.studente)

	tutori_da_approvare = Tutor.objects.filter(approvato = False)
	for tutor in tutori_da_approvare:
		print("Telefono: " + tutor.cellulare)

	query = request.GET.get("q")
	if query:
		tutori_approvati = tutori_approvati.filter(
			Q(studente__nome__icontains = query) |
			Q(studente__cognome__icontains = query) |
			Q(materia__icontains = query)
		).distinct()

	context = {"title": title,
	           "tutori_approvati": tutori_approvati,
	           "tutori_da_approvare": tutori_da_approvare,
	           }

	return render(request, 'tutoring.html', context)


@login_required(login_url = '/login/')
def tutor_form_view(request):
	if not request.user.studente.is_attivato:
		raise Http404
	title = "Proponi tutoring"
	form = TutorForm(request.POST or None)

	if form.is_valid():
		studente = request.user.studente
		cellulare = form.cleaned_data["cellulare"]
		materia = form.cleaned_data["materia"]
		studenti_max = form.cleaned_data["studenti_max"]

		prima = form.cleaned_data["prima"]
		seconda = form.cleaned_data["seconda"]
		terza = form.cleaned_data["terza"]
		quarta = form.cleaned_data["quarta"]
		quinta = form.cleaned_data["quinta"]

		if prima == False and seconda == False and terza == False and quarta == False and quinta == False:
			prima = True
			seconda = True
			terza = True
			quarta = True
			quinta = True

		tutor = Tutor(studente = studente, cellulare = cellulare, materia = materia, studenti_max = studenti_max,
		              prima = prima,
		              seconda = seconda, terza = terza, quarta = quarta, quinta = quinta)
		tutor.save()
		messages.success(request, "Richiesta inviata. Verrà  approvata il più presto possibile",
		                 extra_tags = 'html_safe')

		return HttpResponseRedirect("/tutoring/")

	return render(request, 'form.html', {'title': title, 'form': form})


@login_required(login_url = '/login/')
def approva_tutor(request, id_tutor):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		tutor = Tutor.objects.get(id = id_tutor)
		tutor.approvato = True
		tutor.save()
		return HttpResponseRedirect("/tutoring/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def elimina_tutor(request, id_tutor):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		tutor = Tutor.objects.get(id = id_tutor)
		tutor.delete()
		return HttpResponseRedirect("/tutoring/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def richiedi_tutor(request, id_tutor):
	if not request.user.studente.is_attivato:
		raise Http404
	tutor = Tutor.objects.get(id = id_tutor)
	studente = request.user.studente
	if len(Allievo.objects.filter(tutor = tutor, studente = studente)) > 0:
		messages.success(request, "Hai già inviato una richiesta a questo tutor.", extra_tags = 'html_safe')
		return HttpResponseRedirect("/tutoring/")
	else:
		allievo = Allievo(tutor = tutor, studente = studente)
		allievo.save()
		send_mail('Tutoring',
		          """L'alunno {0} di classe {1}^{2} ha chiesto il tutoring in {3}. \nPer contattarlo, questo è il suo indirizzo email: {4}""".format(
			          studente.nome + " " + studente.cognome, str(studente.classe), studente.sezione, tutor.materia,
			          studente.user.email), 'RighiNetwork <noreply@righi-network.com>',
		          [tutor.studente.user.email])

		return HttpResponseRedirect("/tutoring/")
