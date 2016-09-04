from django.db import models
from django.utils.six import with_metaclass


class UpperCharField(models.CharField):
	def __init__(self, *args, **kwargs):
		self.is_uppercase = kwargs.pop('uppercase', False)
		super(UpperCharField, self).__init__(*args, **kwargs)

	def get_prep_value(self, value):
		value = super(UpperCharField, self).get_prep_value(value)
		if self.is_uppercase:
			return value.upper()

		return value


class IntegerRangeField(models.IntegerField):
	def __init__(self, verbose_name = None, name = None, min_value = None, max_value = None, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		models.IntegerField.__init__(self, verbose_name, name, **kwargs)

	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value': self.max_value}
		defaults.update(kwargs)
		return super(IntegerRangeField, self).formfield(**defaults)
