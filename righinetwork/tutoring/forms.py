from django.forms import ModelChoiceField

from .models import *

class StudenteModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s - %s^ %s" % (obj.nome, obj.cognome, obj.classe, obj.sezione)

class TutorAdminForm(forms.ModelForm):
	studente = StudenteModelChoiceField(Studente.objects.all().order_by("classe", "sezione", "cognome"))

	class Meta:
		model = Tutor
		materia_widget = forms.Select(choices = (
			("latino", "Latino"),
			("fisica", "Fisica"),
			("matematica", "Matematica"),))
		fields = ['studente', 'materia', 'cellulare', 'studenti_max', 'prima', 'seconda', 'terza', 'quarta', 'quinta', 'approvato']
		widgets = {
			'materia': materia_widget,
		}
