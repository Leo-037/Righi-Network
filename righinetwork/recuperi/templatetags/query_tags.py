from django import template
from django.db.models import Count
from recuperi.models import *

register = template.Library()


@register.simple_tag()
def query_gruppi(turno, user):
	gruppi = Gruppo.objects.filter(turno = turno)
	scelti = []

	for gruppo in gruppi:
		if Iscritto.objects.filter(studente = user.studente, gruppo = gruppo):
			scelti.append(gruppo)

	return scelti


@register.simple_tag()
def query_turni(giorno, *args, **kwargs):
	index = kwargs['index']
	print("Indice: " + str(index))
	if int(index) >= 0:
		turni = []
		for turno in Turno.objects.filter(giorno = giorno).order_by('ora'):
			turni.append(turno)
			print("Ciclo for, lunghezza turni: " + str(len(turni)))

		print("Finito for, lunghezza turni: " + str(len(turni)))

		if not index + 1 > len(turni):
			print("Indice maggiore del numero di turni")
			return turni[int(index)]
		else:
			return False

	else:
		query = Turno.objects.filter(giorno = giorno).order_by("ora")
		return query
