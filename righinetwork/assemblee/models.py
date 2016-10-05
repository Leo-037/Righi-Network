from accounts.models import Studente
from django import forms
from django.db import models
from django.forms import ModelForm


class Assemblea(models.Model):
	data_assemblea = models.DateField()
	sede = models.CharField(max_length = 150)

	mostra_assemblea = models.DateField()
	nascondi_assemblea = models.DateField()

	class Meta:
		permissions = (
			("can_add_assemblea", "Può aggiungere un'assemblea"),
			("can_edit_assemblea", "Può modificare un'assemblea"),
			("can_delete_assemblea", "Può rimuovere un'assemblea"),
		)


class Turno(models.Model):
	ora = models.TimeField(verbose_name = "Orario di inizio")
	orario_fine = models.TimeField(verbose_name = "Fine turno")
	assemblea = models.ForeignKey(Assemblea, on_delete = models.CASCADE)


class Gruppo(models.Model):
	titolo = models.TextField()
	aula = models.TextField()
	descrizione = models.TextField()
	host = models.TextField(verbose_name = "Tenuto da ")
	iscritti_massimi = models.PositiveIntegerField()
	iscritti = models.PositiveIntegerField(default = 0)

	turno = models.ForeignKey(Turno, on_delete = models.CASCADE)


class Iscritto(models.Model):
	studente = models.ForeignKey(Studente, related_name = "iscritti_assemblee")
	gruppo = models.ForeignKey(Gruppo, on_delete = models.CASCADE)



class AssembleaForm(ModelForm):
	n_turni = forms.IntegerField(label = "Numero turni", min_value = 0, )

	class Meta:
		model = Assemblea
		data_widget = forms.SelectDateWidget()

		fields = ['sede', 'data_assemblea', 'mostra_assemblea', 'nascondi_assemblea', 'n_turni']
		widgets = {
			'data_assemblea': data_widget,
			'mostra_assemblea': data_widget,
			'nascondi_assemblea': data_widget,
		}


class TurnoForm(ModelForm):
	class Meta:
		model = Turno
		ora_widget = forms.TimeInput()

		fields = ['ora', 'orario_fine', 'assemblea']
		widgets = {
			'ora': ora_widget,
			'orario_fine': ora_widget,
		}


class GruppoForm(ModelForm):
	class Meta:
		model = Gruppo
		text_widget = forms.TextInput()
		fields = ['aula', 'titolo', 'descrizione', 'host', 'iscritti_massimi', 'turno']
		widgets = {
			'aula': text_widget,
			'titolo': text_widget,
			'host': text_widget,
		}


class IscrittoForm(ModelForm):
	class Meta:
		model = Iscritto
		fields = ['studente', 'gruppo']
