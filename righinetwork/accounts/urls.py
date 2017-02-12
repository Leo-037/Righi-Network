from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.classi_view, name = 'login'),
	url(r'^aggiorna/email/$', views.aggiorna_mail_view),
	url(r'^aggiorna/password/$', views.aggiorna_password_view),
	url(r'^(?P<classesezione>[\w-]+)/$', views.dettagli_classe_view),
	url(r"^[\w-]+/elimina_studente/(?P<username>['\w-]+)/$", views.elimina_studente_view),
]
