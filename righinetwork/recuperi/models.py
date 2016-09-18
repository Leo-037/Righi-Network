from accounts.models import Studente
from django.db import models


class Settimana(models.Model):
	data_inizio = models.DateField()
	data_fine = models.DateField()

	mostra_settimana = models.DateField()
	nascondi_settimana = models.DateField()


class Giorno(models.Model):
	data = models.DateField()
	nome = models.CharField(max_length = 9)

	settimana = models.ForeignKey(Settimana)

	class Meta:
		ordering = ('data',)


class Turno(models.Model):
	ora = models.TimeField(verbose_name = "Orario di inizio")
	orario_fine = models.TimeField(verbose_name = "Fine turno")

	giorno = models.ForeignKey(Giorno)


class Gruppo(models.Model):
	titolo = models.TextField()
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

# class AssembleaForm(ModelForm):
# 	class Meta:
# 		model = Assemblea
# 		data_widget = forms.SelectDateWidget()
#
# 		mostra_ass_widget = forms.SelectDateWidget()
# 		nascondi_ass_widget = forms.SelectDateWidget()
#
# 		fields = ['data_assemblea', 'mostra_assemblea', 'nascondi_assemblea']
# 		widgets = {
# 			'data_assemblea': data_widget,
# 			'mostra_assemblea': mostra_ass_widget,
# 			'nascondi_assemblea': nascondi_ass_widget,
# 		}
#
#
# class TurnoForm(ModelForm):
# 	class Meta:
# 		model = Turno
# 		ora_widget = forms.TimeInput()
# 		orario_fine_widget = forms.TimeInput()
# 		fields = ['ora', 'orario_fine', 'assemblea']
# 		widgets = {
# 			'ora': ora_widget,
# 			'orario_fine': orario_fine_widget,
# 		}
#
#
# class GruppoForm(ModelForm):
# 	class Meta:
# 		model = Gruppo
# 		fields = ['aula', 'titolo', 'descrizione', 'host', 'iscritti_massimi', 'turno']
#
#
# class IscrittoForm(ModelForm):
# 	class Meta:
# 		model = Iscritto
# 		fields = ['studente', 'gruppo']
