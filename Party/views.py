# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Party

# Create your views here.

def party_list_view(request):
	"""docstring for PartyList"""

	template_name = 'party_index.html'
	context_object_name = 'party'

	context = {}

	party_list = []

	party_class = Party()
	parties = party_class.getAll()

	for party in parties:

		# unsure how to handle this, maybe encode?
		#  Also, there do not appear to be any members from this party in the DB
		#   Possibly bad data?
		if party[0]['name'].strip().upper() == "D/PNP":
			continue
		party_list.append(party[0]['name'])

	context = {'parties': party_list}
	return render(request, template_name, context)

def party_detail(request, name):
	template_name = 'party_detail.html'

	context = {}

	party_dict = {'R': 'Republican',
	'D': 'Democratic',
	'I': 'Independant',
	'NPP': '...',
	'DFL': 'Democratic Farm Labor Party',
	'I THEN R': 'Independant THEN Republican',
	'I THEN D': 'Independant THEN Democratic',
	'D THEN R': 'Democratic THEN Republican',
	'R THEN D': 'Republican THEN Democratic',
	'UNKNOWN': 'UNKNOWN',
	'R THEN I': 'Republican THEN Independant',
	'D THEN I': 'Democratic THEN Independant',
	}

	party = Party().getSingleByName(name)

	context['party'] = party_dict[name]
	context['party_abbreviation'] = name

	return render(request, template_name, context)

def party_members(request, name):
	template_name = 'party_members.html'
	member_list = []

	party_dict = {'R': 'Republican',
	'D': 'Democratic',
	'I': 'Independant',
	'NPP': '...',
	'DFL': 'Democratic Farm Labor Party',
	'I THEN R': 'Independant THEN Republican',
	'I THEN D': 'Independant THEN Democratic',
	'D THEN R': 'Democratic THEN Republican',
	'R THEN D': 'Republican THEN Democratic',
	'UNKNOWN': 'Unknown',
	'R THEN I': 'Republican THEN Independant',
	'D THEN I': 'Democratic THEN Independant',
	}

	context = {'party': party_dict[name],
			   'party_abbreviation': name,
			   'member_list': member_list
			}

	members = Party().getPartyMembers(name)

	for member in members:
		member_list.append(member)

	return render(request, template_name, context)

