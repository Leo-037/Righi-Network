from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Studente


class StudenteInline(admin.StackedInline):
	model = Studente
	can_delete = False
	verbose_name_plural = 'Studenti'


class StudenteModelAdmin(admin.ModelAdmin):
	list_display = ["user", "email", "nome", "cognome", "classe", "sezione", "rappr_classe", "rappr_istituto"]
	list_display_links = ["user"]
	list_filter = ["classe", "sezione", "is_rappr_classe", "is_rappr_istituto"]
	search_fields = ["classe", "sezione", "is_rappr_classe", "is_rappr_istituto"]

	def rappr_classe(self, obj):
		return obj.is_rappr_classe
	rappr_classe.short_description = "Rappresentante di classe"
	rappr_classe.boolean = True

	def rappr_istituto(self, obj):
		return obj.is_rappr_istituto
	rappr_istituto.short_description = "Rappresentante d'istituto"
	rappr_istituto.boolean = True

	def email(self, obj):
		return obj.user.email

	class Meta:
		model = Studente
		verbose_name = "Studente"
		verbose_name_plural = "Studenti"

class UserAdmin(BaseUserAdmin):
	list_display = ["username", "email", "is_staff"]
	inlines = (StudenteInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Studente, StudenteModelAdmin)
