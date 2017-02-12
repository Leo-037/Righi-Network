import locale

from chartit import DataPool, Chart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from .models import *


# CREATE

@login_required(login_url = '/login/')
def aggiorna_bilancio_view(request):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		title = "Aggiorna bilancio"
		if request.method == "GET":
			form = BilancioForm()
			return render(request, 'form.html', {'title': title, 'form': form})
		elif request.method == "POST":
			form = BilancioForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect("/bilancio/")
	else:
		raise Http404


# RETRIEVE

@login_required(login_url = '/login/')
def bilancio_chart_view(request):
	if not request.user.studente.is_attivato:
		raise Http404
	title = "Bilancio"

	data = DataPool(
		series = [{'options': {
			'source': BilancioMensileFondo.objects.all()},
			'terms': [
				'data',
				# 'descrizione',
				'bilancio']}
		])

	def format_data(*t):
		data_da_formattare = t[0]
		mesi = {'01': 'Gen','02': 'Feb', '03': 'Mar', '04': 'Apr',
            		'05': 'Mag', '06': 'Giu', '07': 'Lug', '08': 'Ago',
            		'09': 'Set', '10': 'Ott', '11': 'Nov', '12': 'Dic'}
		numero_mese = data_da_formattare.strftime("%m")
		mese = mesi[numero_mese]
		giorno = data_da_formattare.strftime("%d")
		anno = data_da_formattare.strftime("%Y")
		data_formattata = str(giorno + " " + mese + " " + anno)
		return (data_formattata)

	cht = Chart(
		datasource = data,
		series_options =
		[{'options': {
			'type': 'line',
			'stacking': False, },
			'terms': {
				'data': [
					'bilancio', ]
			}}],
		chart_options =
		{'title': {
			'text': 'Bilancio fondo studentesco'},
			'tooltip': {'backgroundColor': '#FFFFFF',
			            # 'formatter': tooltip_format,
			            'pointFormat': '<tr><td style="color: {series.color}">Bilancio: </td>' +
			                           '<td style="text-align: right"><b>{point.y} €</b></td></tr>',
			            'footerFormat': '</table>',
			            },
			'xAxis': {
				'title': {
					'text': 'Data'}},
			'yAxis': {
				'title': {
					'text': 'Bilancio'}},
		},
		x_sortf_mapf_mts = (None, format_data, False)
	)

	date = BilancioMensileFondo.objects.all().order_by('-data')

	return render(request, 'bilancio.html', context = {'title': title, 'chart': cht, 'date': date})


# UPDATE

@login_required(login_url = '/login/')
def update_bilancio_view(request, id_bilancio):
	if not request.user.studente.is_rappr_istituto and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(BilancioMensileFondo, id = id_bilancio)
	form = BilancioForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "<h4><a href='#'>Bilancio</a> salvato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/bilancio/")

	context = {
		"title": "Modifica bilancio",
		"instance": instance,
		"form": form,
	}
	return render(request, "form.html", context)


# DELETE

@login_required(login_url = '/login/')
def delete_bilancio_view(request, id_bilancio):
	if request.user.studente.is_rappr_istituto or request.user.is_superuser:
		instance = get_object_or_404(BilancioMensileFondo, id = id_bilancio)
		instance.delete()
		messages.success(request, "<h4>Cancellato</h4>", extra_tags = 'html_safe')
		return HttpResponseRedirect("/bilancio/")
	else:
		raise Http404
