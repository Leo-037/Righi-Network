from accounts.models import Studente
from django import forms
from django.db import models
from django.forms import ModelForm


class Settimana(models.Model):
	data_inizio = models.DateField()
	data_fine = models.DateField()

	mostra_settimana = models.DateField()
	nascondi_settimana = models.DateField()


class Giorno(models.Model):
	data = models.DateField()
	nome = models.CharField(max_length = 9, verbose_name = "Giorno")

	settimana = models.ForeignKey(Settimana)

	class Meta:
		ordering = ('data',)


class Turno(models.Model):
	ora = models.TimeField(verbose_name = "Orario di inizio")
	orario_fine = models.TimeField(verbose_name = "Fine turno")

	giorno = models.ForeignKey(Giorno)


class Gruppo(models.Model):
	titolo = models.TextField()
	CHOICES = (("Sede", "Sede Viale Pepoli"),("Succursale", "Succursale Via Tolmino"))
	sede = models.CharField(max_length = 150, choices = CHOICES)
	aula = models.TextField()
	descrizione = models.TextField()
	host = models.TextField(verbose_name = "Tenuto da ")
	iscritti_massimi = models.PositiveIntegerField()
	iscritti = models.PositiveIntegerField(default = 0)

	recupero = models.BooleanField(default = False, blank = False, null = False)

	turno = models.ForeignKey(Turno)


class Iscritto(models.Model):
	studente = models.ForeignKey(Studente, related_name = "iscritti_recuperi")
	gruppo = models.ForeignKey(Gruppo)


class SettimanaForm(ModelForm):
	class Meta:
		model = Settimana
		data_widget = forms.SelectDateWidget()

		fields = ['data_inizio', 'data_fine', 'mostra_settimana', 'nascondi_settimana']
		widgets = {
			'data_inizio': data_widget,
			'data_fine': data_widget,
			'mostra_settimana': data_widget,
			'nascondi_settimana': data_widget
		}


class GiornoForm(ModelForm):
	n_turni = forms.IntegerField(label = "Numero turni", min_value = 0, )

	class Meta:
		models = Giorno
		data_widget = forms.DateField()
		fields = ['data', 'nome', 'settimana']
		widgets = {
			'data': data_widget,
		}


class TurnoForm(ModelForm):
	class Meta:
		model = Turno
		ora_widget = forms.TimeInput()

		fields = ['ora', 'orario_fine', 'giorno']
		widgets = {
			'ora': ora_widget,
			'orario_fine': ora_widget,
		}


class GruppoForm(ModelForm):
	class Meta:
		model = Gruppo
		text_widget = forms.TextInput()
		fields = ['sede', 'aula', 'titolo', 'descrizione', 'host', 'iscritti_massimi', 'recupero', 'turno']
		widgets = {
			'aula': text_widget,
			'titolo': text_widget,
			'host': text_widget,
		}


class IscrittoForm(ModelForm):
	class Meta:
		model = Iscritto
		fields = ['studente', 'gruppo']
