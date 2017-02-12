from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
)

from .models import *

# from allauth.account.forms import LoginForm, SignupForm

User = get_user_model()


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("Questo utente non esiste")
			if not user.check_password(password):
				raise forms.ValidationError("Password Incorretta")
			if not user.is_active:
				raise forms.ValidationError("Questo utente non è più attivo")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class ClasseForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(ClasseForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-inline'
		self.helper.field_template = 'bootstrap3/layout/inline_field.html'
		self.helper.form_method = 'POST'
		self.helper.layout = Layout(Div(
			'classe',
			'sezione',
			Submit('Aggiungi Classe', 'Aggiungi Classe', css_class = 'btn-primary')
		))

	classe = forms.IntegerField(min_value = 1, max_value = 5)
	sezione = forms.CharField(max_length = 1)

	def clean_sezione(self):
		sezione = self.cleaned_data.get('sezione')
		sezione.upper()
		return sezione


class StudenteRegisterForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StudenteRegisterForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-inline'
		self.helper.field_template = 'bootstrap3/layout/inline_field.html'
		self.helper.form_method = 'POST'
		self.helper.add_input(Submit('Aggiungi Studente', 'Aggiungi Studente', css_class = 'btn-primary'))
		self.helper.layout = Layout(
			'username',
			'nome',
			'cognome',
			'classe',
			'sezione',
			'password',
		)

	nome = forms.CharField(label = 'Nome')
	cognome = forms.CharField(label = 'Cognome')
	classe = forms.IntegerField(min_value = 1, max_value = 5)
	sezione = forms.CharField(max_length = 1)
	password = forms.CharField(widget = forms.PasswordInput, label = 'Password')

	class Meta:
		model = User
		fields = [
			'username',
			'nome',
			'cognome',
			'classe',
			'sezione',
			'password',
		]

	def clean_sezione(self):
		sezione = self.cleaned_data.get('sezione')
		sezione.upper()
		return sezione


class CambiaPasswordForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(CambiaPasswordForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		# self.helper.form_class = 'form-inline'
		# self.helper.field_template = 'bootstrap3/layout/inline_field.html'
		self.helper.form_method = 'POST'
		self.helper.add_input(Submit('Aggiorna Account', 'Aggiorna Account'))
		self.helper.layout = Layout(
			'codice_mail',
			'password',
			'password2',
		)


	codice_mail = forms.CharField(label = 'Inserisci codice')
	password = forms.CharField(widget = forms.PasswordInput, label = 'Password')
	password2 = forms.CharField(widget = forms.PasswordInput, label = 'Conferma Password')

	class Meta:
		model = User
		fields = [
			'codice_mail',
			'password',
			'password2',
		]

	def clean_codice_mail(self):
		codice_inserito = self.cleaned_data.get('codice_mail')
		codice_corretto = self.request.session.get('codice_mail')
		if codice_inserito != codice_corretto:
			raise forms.ValidationError("Codice non corretto")
		return codice_corretto

	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Le password devono coincidere")
		return password


class MailForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(MailForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.add_input(Submit('Invia Codice', 'Invia Codice', css_class = 'btn-primary'))
		self.helper.layout = Layout(
			'email',
			'email2',
		)

	email = forms.EmailField(label = 'Indirizzo Email')
	email2 = forms.EmailField(label = 'Conferma Email')

	class Meta:
		model = User
		fields = [
			'email',
			'email2'
		]


	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Le mail devono coincidere")
		email_qs = User.objects.filter(email = email)
		if email_qs.exists():
			raise forms.ValidationError("Questa email è già stata registrata")
		return email


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(label = 'Indirizzo Email')
	email2 = forms.EmailField(label = 'Conferma Email')
	password = forms.CharField(widget = forms.PasswordInput, label = 'Password')
	password2 = forms.CharField(widget = forms.PasswordInput, label = 'Conferma Password')
	nome = forms.CharField(label = 'Nome')
	cognome = forms.CharField(label = 'Cognome')
	classe = forms.IntegerField(min_value = 1, max_value = 5)
	sezione = forms.CharField(max_length = 1)

	class Meta:
		model = User
		fields = [
			'username',
			'nome',
			'cognome',
			'classe',
			'sezione',
			'email',
			'email2',
			'password',
			'password2',
		]

	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Le mail devono coincidere")
		email_qs = User.objects.filter(email = email)
		if email_qs.exists():
			raise forms.ValidationError("Questa email è già stata registrata")
		return email

	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Le password devono coincidere")
		return password

	def clean_sezione(self):
		sezione = self.cleaned_data.get('sezione')
		sezione.upper()
		return sezione
