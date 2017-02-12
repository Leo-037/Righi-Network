from accounts.views import login_view, logout_view
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

# from tutoring.views import view

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^gestione/', include('accounts.urls', namespace = 'accounts')),
	url(r'^assemblee/', include('assemblee.urls', namespace = 'assemblee')),
	url(r'^bilancio/', include('bilancio.urls', namespace = 'bilancio')),
	url(r'^login/$', login_view, name = "login"),
	url(r'^logout/$', logout_view, name = "logout"),
	url(r'^recuperi/', include('recuperi.urls', namespace = 'recuperi')),
	url(r'^times/', include('times.urls', namespace = 'times')),
	url(r'^tutoring/', include("tutoring.urls", namespace = 'tutoring')),
	url(r'^password-dimenticata/', include('password_reset.urls')),
	url(r'^', include('posts.urls', namespace = 'posts')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)