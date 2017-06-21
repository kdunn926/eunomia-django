# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Monologue

# Create your views here.

def monologues_by_date(request, date):
	"""docstring for PartyList"""

	template_name = 'monologues_by_date.html'
	context_object_name = 'monologues'

	context = {}

	tuple_monologues = Monologue().getMonloguesByDate(date)
	monologues = [m[0] for m in tuple_monologues]
	congress_number = monologues[1]['congressionalYear']

	senate_monologues = []
	house_monologues = []

	for m in monologues:
		if m['branch'].lower() == 'house':
			house_monologues.append(m)
		elif m['branch'].lower() == 'senate':
			senate_monologues.append(m)
			#print m['text']
		else:
			print "I AM CONFUSED...."

	context = {'monologues': monologues, 'congress_number':congress_number, 'date': date,
				'senate_monologues':senate_monologues, 'house_monologues': house_monologues}

	return render(request, template_name, context)

def monologue_detail(request, id):
	template_name = 'monologue_detail.html'
	context_object_name = 'monologues'

	context = {}

	monologues = Monologue().getMonologueById(id)
	context['monologue_info'] = monologues
	#monologues = [m[0] for m in tuple_monologues]
	print monologues.keys()
	#congress_number = monologues[1]['congressionalYear']

	#senate_monologues = []
	#house_monologues = []

	#for m in monologues:
	#	if m['branch'].lower() == 'house':
	#		house_monologues.append(m)
	#	elif m['branch'].lower() == 'senate':
	#		senate_monologues.append(m)
			#print m['text']
	#	else:
	#		print "I AM CONFUSED...."

	#context = {'monologues': monologues, 'congress_number':congress_number, 'date': date,
	#			'senate_monologues':senate_monologues, 'house_monologues': house_monologues}

	return render(request, template_name, context)
