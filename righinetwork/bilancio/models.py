from django.db import models
from django.forms import ModelForm
from django import forms
# Create your models here.

class BilancioMensileFondo(models.Model):
	data = models.DateField()
	descrizione = models.TextField()
	bilancio = models.DecimalField(max_digits = 8, decimal_places = 2)

class BilancioForm(ModelForm):
	class Meta:
		model = BilancioMensileFondo
		data_widget = forms.SelectDateWidget()

		fields = ['data', 'descrizione', 'bilancio']
		widgets = {
			'data': data_widget,
		}
