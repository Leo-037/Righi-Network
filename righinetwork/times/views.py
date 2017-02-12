import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from .models import *


# CREATE

@login_required(login_url = '/login/')
def aggiungi_issue_view(request):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser or request.user.studente.is_caporedattore:
		title = "Crea numero Righi Times"
		if request.method == "GET":
			form = IssueForm()
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = IssueForm(request.POST)
			if form.is_valid():
				issue = form.save()
				return HttpResponseRedirect("/times/" + str(issue.slug) + "/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def aggiungi_articolo_view(request, slug = None):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser or request.user.studente.is_caporedattore:
		title = "Aggiungi articolo"
		if request.method == "GET":
			issue = get_object_or_404(Issue, slug = slug)
			form = ArticleForm(request.POST or None, request.FILES or None, initial = {'issue': issue})
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = ArticleForm(request.POST or None, request.FILES or None)
			print(form.is_valid())
			if form.is_valid():
				articolo = form.save()
				print(articolo)
				return HttpResponseRedirect("/times/" + str(articolo.issue.slug) + "/articolo/" + str(articolo.slug) + "/")
	else:
		raise Http404


# RETRIEVE

@login_required(login_url = '/login/')
def times_view(request):  # mostra numeri righitimes
	if not request.user.studente.is_attivato:
		raise Http404
	title = "Righi Times"
	today = time.strftime("%Y-%m-%d")
	issues = Issue.objects.filter().order_by('-data')

	context = {'issues': issues,
	           'title': title
	           }
	return render(request, 'times.html', context)


@login_required(login_url = '/login/')
def issue_view(request, slug = None):  # mostra articoli in un numero
	if not request.user.studente.is_attivato:
		raise Http404
	issue = get_object_or_404(Issue, slug = slug)
	articoli = Article.objects.filter(issue = issue)
	context = {'issue': issue,
	           'articoli': articoli,
	           }
	return render(request, 'issue.html', context)


@login_required(login_url = '/login/')
def articolo_view(request, slug = None):  # mostra un articolo
	if not request.user.studente.is_attivato:
		raise Http404
	articolo = get_object_or_404(Article, slug = slug)
	issue = Issue.objects.get(id = articolo.issue.id)

	title = str(articolo.titolo)

	context = {'articolo': articolo,
	           'issue': issue,
	           'title': title,
	           }

	return render(request, 'articolo.html', context)


# UPDATE

@login_required(login_url = '/login/')
def update_issue_view(request, slug = None):
	if not request.user.studente.is_rappr_istituto and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Issue, slug = slug)
	form = IssueForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "<h4><a href='#'>Numero RighiTimes</a> salvato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/times/" + str(instance.slug) + "/")

	context = {
		"title": "Modifica numero",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


@login_required(login_url = '/login/')
def update_articolo_view(request, slug = None):
	if not request.user.studente.is_rappr_istituto and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Article, slug = slug)
	form = ArticleForm(request.POST or None, request.FILES or None, instance = instance,
	                   initial = {'issue': instance.issue})
	form.fields['issue'].widget = forms.HiddenInput()
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "<h4><a href='#'>Articolo</a> salvato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/times/" + str(instance.issue.slug) + "/articolo/" + str(instance.slug) + "/")

	context = {
		"title": "Modifica turno",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


# DELETE

@login_required(login_url = '/login/')
def delete_issue_view(request, slug = None):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		issue = Issue.objects.get(slug = slug)
		issue.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/times/")
	else:
		raise Http404


@login_required(login_url = '/login/')
def delete_articolo_view(request, slug = None):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		articolo = Article.objects.get(slug = slug)
		articolo.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/times/" + str(articolo.issue.slug) + "/")
	else:
		raise Http404
