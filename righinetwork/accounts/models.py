from django.contrib.auth.models import User
from django.db import models

from .custom_models import IntegerRangeField, UpperCharField


class Studente(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)

	nome = models.CharField(max_length = 25)
	cognome = models.CharField(max_length = 25)

	classe = IntegerRangeField(min_value = 1, max_value = 5)
	sezione = UpperCharField(max_length = 1, uppercase = True)

	is_rappr_classe = models.BooleanField(default = False)
	is_rappr_istituto = models.BooleanField(default = False)
	is_caporedattore = models.BooleanField(default = False)

	is_attivato = models.BooleanField(default = False)
	password = models.CharField(max_length = 10, blank = True)
