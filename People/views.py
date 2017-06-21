# Create your views here.
from django.shortcuts import render
from django.views import generic

from .models import Person
from Congress.models import Congress
from Party.models import Party
from Monologues.models import Monologue

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


def person_detail(request, name):
	template_name = 'person_detail.html'

	monologues = Monologue().getMonologueSpokenBy(name)
	parties = Person().getParty(name)
	congress = Congress().getCongressSession(name)
	state = Person().getState(name)

	#import time

	#start_time = time.time()
	#monologue_list = []

	#TODO
	# fix sort, sort by date and sequence

	for monologue_text, monologue_id in monologues:
		#print monologue
		monologue_dict = {}
		date, house, session, text, sequence = monologue_id.split("-")

		#monologue = Monologue().getMonologueById(monologue_id[0].encode('utf-8'))

		monologue_dict['date'] = date.encode('utf-8')
		monologue_dict['house'] = house.encode('utf-8')
		monologue_dict['session'] = session.encode('utf-8')
		monologue_dict['sequence'] = sequence.encode('utf-8')
		monologue_dict['monologue'] = monologue_text
		#monologue_list.append(monologue_dict)

	#end_time = time.time()
	#print "Parsed %s monolouges in %s seconds" % (str(len(monologue_list)), str(end_time - start_time))

	state_list = list(set([states[0].encode('utf-8') for states in state]))
	congress_list = list(set([congress_session[0].encode('utf-8') for congress_session in congress]))
	party_list = list(set([party[0].encode('utf-8') for party in parties]))

	context = {'Sessions': congress_list,
				'Monologues': monologues,
				'Party': party_list,
				'State': state_list,
				'Name': name}
	return render(request, template_name, context)

