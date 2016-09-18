from django.contrib import admin

from .forms import TutorAdminForm
from .models import Tutor


class TutorModelAdmin(admin.ModelAdmin):
	list_display = ["mostra_studente", "materia", "studenti_max", "prima", "seconda", "terza", "quarta", "quinta",
	                "approvato", "cellulare"]
	list_filter = ["studente", "materia", "prima", "seconda", "terza", "quarta", "quinta", "approvato"]
	list_search = ["studente", "materia", "prima", "seconda", "terza", "quarta", "quinta", "approvato"]

	def mostra_studente(self, obj):
		return str(obj.studente.nome)

	form = TutorAdminForm

	class Meta:
		model = Tutor
		verbose_name_plural = "Tutor"


admin.site.register(Tutor, TutorModelAdmin)
