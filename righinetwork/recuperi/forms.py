from django.forms import ModelChoiceField
from django import forms

from .models import *


class SettimanaModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s: %s - %s" % (obj.id, obj.data_inizio, obj.data_fine)


class GiornoModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s - %s" % (obj.nome, obj.data)


class TurnoModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s dalle %s alle %s, settimana dal %s al %s" % (obj.giorno.nome, obj.giorno.data, obj.ora, obj.orario_fine, obj.giorno.settimana.data_inizio, obj.giorno.settimana.data_fine)


class GruppoModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s" % (obj.titolo)


class StudenteModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s - %s^ %s" % (obj.nome, obj.cognome, obj.classe, obj.sezione)


class GiornoAdminForm(forms.ModelForm):
	settimana = SettimanaModelChoiceField(Settimana.objects.all().order_by('data_inizio'))

	class Meta:
		model = Giorno
		data_widget = forms.DateInput()
		fields = ['data', 'nome', 'settimana']
		widgets = {
			'data': data_widget,
		}


class TurnoAdminForm(forms.ModelForm):
	giorno = GiornoModelChoiceField(Giorno.objects.all().order_by('data'))

	class Meta:
		model = Turno
		ora_widget = forms.TimeInput()
		orario_fine_widget = forms.TimeInput()
		fields = ['ora', 'orario_fine', 'giorno']
		widgets = {
			'ora': ora_widget,
			'orario_fine': orario_fine_widget,
		}


class GruppoAdminForm(forms.ModelForm):
	turno = TurnoModelChoiceField(Turno.objects.all().order_by('ora'))
	aula = forms.CharField(max_length = 150)
	titolo = forms.CharField(max_length = 150)
	host = forms.CharField(max_length = 150)

	class Meta:
		model = Gruppo
		fields = ['aula', 'titolo', 'descrizione', 'host', 'iscritti_massimi', 'recupero', 'turno']


class IscrittoAdminForm(forms.ModelForm):
	studente = StudenteModelChoiceField(Studente.objects.all())
	gruppo = GruppoModelChoiceField(Gruppo.objects.all())

	class Meta:
		model = Iscritto
		fields = ['studente', 'gruppo']
