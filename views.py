# Create your views here.
from django.shortcuts import render
from django.views import generic

from .models import Person, Party
#from CongressionalRecord import db
import time

#class PeopleListView(generic.ListView):
#    template_name = 'people_index.html'
#    context_object_name = 'people_list'
#    model = Person

def index(request):
	template_name = 'people_index.html'
	context_object_name = 'people_list'

	person_class = Person()

	people_dict = person_class.getAll()

	person_list = []
	context = { 'person_list': person_list }

	for people in people_dict:
		person_list.append(people)

	return render(request, template_name, context)

def party_list_view(request):
	"""docstring for PartyList"""

	template_name = 'party_index.html'
	context_object_name = 'party'

	context = {}

	party_list = []
	context = {'parties': party_list}

	party_class = Party()
	parties = party_class.getAll()
	for party in parties:
		party_list.append(party[0]['name'])

	return render(request, template_name, context)


def person_detail(request, pk):
	print "Should add a person detail page -- think !"
	template_name = 'person_detail.html'

	context = {}
	return render(request, template_name, context)

def party_detail(request, name):
	print "Should add a party detail page -- think !"
	template_name = 'party_detail.html'

	context = {}

	party_dict = {'R': 'Republican',
	'D': 'Democratic',
	'I': 'Independant',
	'NPP': '...',
	'DFL': 'Democratic Farm Labor Party',
	'I then R': 'Independant then Republican',
	'I then D': 'Independant then Democratic',
	'D then R': 'Democratic then Republican',
	'R then D': 'Republican then Democratic',
	'Unknown': 'Unknown',
	'R then I': 'Republican then Independant',
	'D then I': 'Democratic then Independant',
	}

	party = Party().getSingleByName(name)

	context['party'] = party_dict[name]
	context['party_abbreviation'] = name

	return render(request, template_name, context)

def party_members(request, name):
	print "Should add a party member page -- think !"
	template_name = 'party_members.html'
	member_list = []

	party_dict = {'R': 'Republican',
	'D': 'Democratic',
	'I': 'Independant',
	'NPP': '...',
	'DFL': 'Democratic Farm Labor Party',
	'I then R': 'Independant then Republican',
	'I then D': 'Independant then Democratic',
	'D then R': 'Democratic then Republican',
	'R then D': 'Republican then Democratic',
	'Unknown': 'Unknown',
	'R then I': 'Republican then Independant',
	'D then I': 'Democratic then Independant',
	}

	context = {'party': party_dict[name],
			   'party_abbreviation': name,
			   'member_list': member_list
			}

	members = Party().getPartyMembers(name)

	for member in members:
		member_list.append(member)

	return render(request, template_name, context)

