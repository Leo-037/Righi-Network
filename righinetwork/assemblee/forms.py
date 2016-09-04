from django.forms import ModelChoiceField

from .models import *


class AssembleaModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s: %s" % (obj.id, obj.data_assemblea)


class TurnoModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s alle %s, assemblea del %s" % (obj.ora, obj.orario_fine, obj.assemblea.data_assemblea)


class GruppoModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s" % (obj.titolo)


class StudenteModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s - %s^ %s" % (obj.nome, obj.cognome, obj.classe, obj.sezione)


class TurnoAdminForm(forms.ModelForm):
	assemblea = AssembleaModelChoiceField(Assemblea.objects.all().order_by('data_assemblea'))

	class Meta:
		model = Turno
		ora_widget = forms.TimeInput()
		orario_fine_widget = forms.TimeInput()
		fields = ['ora', 'orario_fine', 'assemblea']
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
		fields = ['aula', 'titolo', 'descrizione', 'host', 'iscritti_massimi', 'turno']


class IscrittoAdminForm(forms.ModelForm):
	studente = StudenteModelChoiceField(Studente.objects.all())
	gruppo = GruppoModelChoiceField(Gruppo.objects.all())

	class Meta:
		model = Iscritto
		fields = ['studente', 'gruppo']
