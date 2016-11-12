from accounts.models import Studente
from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.forms import ModelForm


class Tutor(models.Model):
	studente = models.ForeignKey(Studente)

	materia = models.CharField(max_length = 15)

	studenti_max = models.PositiveIntegerField(verbose_name = "Numero massimo studenti")
	n_studenti = models.PositiveIntegerField(blank = True, null = True)

	prima = models.BooleanField(default = True)
	seconda = models.BooleanField(default = True)
	terza = models.BooleanField(default = True)
	quarta = models.BooleanField(default = True)
	quinta = models.BooleanField(default = True)

	approvato = models.BooleanField(default = False)

	phone_regex = RegexValidator(regex = r'^\+(?:[0-9]●?){6,14}[0-9]$',
	                             message = "Il numero di telefono deve essere inserito in questo formato: '+999999999'. Hai aggiunto il +39?")
	cellulare = models.CharField(validators = [phone_regex], verbose_name = "Numero di cellulare", max_length=15)


class Allievo(models.Model):
	tutor = models.ForeignKey(Tutor)
	studente = models.ForeignKey(Studente)


class TutorForm(ModelForm):
	class Meta:
		model = Tutor
		materia_widget = forms.Select(choices = (
			("latino", "Latino"),
			("fisica", "Fisica"),
			("matematica", "Matematica")))
		fields = ['materia', 'cellulare', 'studenti_max', 'prima', 'seconda', 'terza', 'quarta', 'quinta']
		widgets = {
			'materia': materia_widget,
		}
