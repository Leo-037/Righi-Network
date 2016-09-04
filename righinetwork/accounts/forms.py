from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
)



from .custom_models import IntegerRangeField, UpperCharField
from .models import *

User = get_user_model()


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		# user_qs = User.objects.filter(username=username)
		# if user_qs.count() == 1:
		#     user = user_qs.first()
		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("Questo utente non esiste")
			if not user.check_password(password):
				raise forms.ValidationError("Password Incorretta")
			if not user.is_active:
				raise forms.ValidationError("Questo utente non è più attivo")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
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