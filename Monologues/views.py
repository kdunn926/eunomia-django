# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponseForbidden, HttpResponse

from .models import Monologue

import json

# Create your views here.

def monologues_by_date(request, date):
	"""docstring for PartyList"""

	template_name = 'monologues_by_date.html'
	context_object_name = 'monologues'

	context = {}

	tuple_monologues = Monologue().getMonloguesByDate(date)
	monologues = [m[0] for m in tuple_monologues]
	try:
		congress_number = monologues[1]['congressionalYear']
	except IndexError:
		congress_number = monologues[0]['congressionalYear']
	finally:
		congress_number = ''


	senate_monologues = []
	house_monologues = []

	for m in monologues:
		m['speaker'] = m['speaker'].replace("^", "").replace(":", "").replace("(", "").replace(")", "").replace("'", "")
		if m['branch'].lower() == 'house':
			house_monologues.append(m)
		elif m['branch'].lower() == 'senate':
			senate_monologues.append(m)
		else:
			print "I AM CONFUSED...."

	context = {'monologues': monologues, 'congress_number':congress_number, 'date': date,
				'senate_monologues':senate_monologues, 'house_monologues': house_monologues}

	return render(request, template_name, context)

def monologue_detail(request, id):
	template_name = 'monologue_detail.html'
	context_object_name = 'monologues'
	context = {}

	if request.method == 'GET':
		if request.is_ajax():

			monologues = Monologue().getMonologueById(id)

			# Reformat the word histogram for better parsing in the JavaScript
			wordHistogram = monologues['wordHistogram'].encode('utf-8').strip("'").strip("[").strip("]").strip().split(",")
			word_count_dict = {}
			for word_count in wordHistogram:
			 	word, count = word_count.split(":")
			 	word = word.strip().strip("'")
			 	count = count.strip().strip("'")
			 	word_count_dict[word] = count

			monologues['wordHistogram'] = word_count_dict

			data = json.dumps(monologues)
			return HttpResponse(data, content_type='json')

		else:
			monologues = Monologue().getMonologueById(id)
			context['monologue_info'] = monologues
			return render(request, template_name, context)

		return redirect(request['HTTP_REFERRER'])
	return redirect(request['HTTP_REFERRER'])
