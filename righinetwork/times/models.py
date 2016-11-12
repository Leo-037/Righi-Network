from autoslug import AutoSlugField
from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils.text import slugify

from accounts.models import Studente


# Create your models here.
class Issue(models.Model):
	data = models.DateField()
	slug = AutoSlugField(populate_from = 'data', unique = True)


def upload_location(instance, filename):
	ArticleModel = instance.__class__
	try:
		new_id = ArticleModel.objects.order_by("id").last().id + 1
	except:
		new_id = 1

	extension = filename.split(".")[-1]
	if extension != "pdf":
		pass

	return "articoli/%s/%s" % (new_id, instance.titolo + "." + str(extension))


class Article(models.Model):
	titolo = models.CharField(max_length = 150)
	contenuto = models.FileField("File - SOLO PDF", upload_to = upload_location,
	                             null = True,
	                             blank = True)
	autore = models.CharField(max_length = 150)

	issue = models.ForeignKey(Issue, on_delete = models.CASCADE)

	slug = AutoSlugField(populate_from = 'titolo', unique_with = ('titolo', 'issue'))


class Writer(models.Model):
	studente = models.OneToOneField(Studente)
	articolo = models.ManyToManyField(Article)


class IssueForm(ModelForm):
	class Meta:
		model = Issue
		data_widget = forms.SelectDateWidget()

		fields = ['data']
		widgets = {
			'data': data_widget,
		}


class ArticleForm(ModelForm):
	class Meta:
		model = Article

		fields = ['titolo', 'contenuto', 'autore', 'issue']

	# def clean(self):
	# 	articolo = self.cleaned_data
	# 	if articolo['contenuto'].filename.split(".")[-1] != "pdf":
	# 		raise forms.ValidationError("Solo pdf ammessi")
