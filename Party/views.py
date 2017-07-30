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

	party_dict = {'R': ('Republican','https://en.wikipedia.org/wiki/Republican_Party_(United_States)'),
	'D': ('Democratic', 'https://en.wikipedia.org/wiki/Democratic_Party_(United_States)'),
	'I': ('Independant',''),
	'NPP': '...',
	'DFL': ('Democratic Farm Labor Party','https://en.wikipedia.org/wiki/Minnesota_Democratic%E2%80%93Farmer%E2%80%93Labor_Party'),
	'I then R': ('Independant THEN Republican',''),
	'I then D': ('Independant THEN Democratic',''),
	'D then R': ('Democratic THEN Republican',''),
	'R then D': ('Republican THEN Democratic',''),
	'UNKNOWN': ('UNKNOWN',''),
	'R then I': ('Republican THEN Independant',''),
	'D then I': ('Democratic THEN Independant','')
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
	'I then R': 'Independant THEN Republican',
	'I then D': 'Independant THEN Democratic',
	'D then R': 'Democratic THEN Republican',
	'R then D': 'Republican THEN Democratic',
	'UNKNOWN': 'Unknown',
	'R then I': 'Republican THEN Independant',
	'D then I': 'Democratic THEN Independant',
	}

	context = {'party': party_dict[name],
			   'party_abbreviation': name,
			   'member_list': member_list
			}

	members = Party().getPartyMembers(name)

	for member in members:
		member_list.append(member)

	return render(request, template_name, context)

