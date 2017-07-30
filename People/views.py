# Create your views here.
from django.shortcuts import render, redirect
from django.views import generic

from .models import Person
from Congress.models import Congress
from Party.models import Party
from Monologues.models import Monologue

import re
import random

#class PeopleListView(generic.ListView):
#    template_name = 'people_index.html'
#    context_object_name = 'people_list'
#    model = Person

def index(request):
	template_name = 'people_index.html'
	context_object_name = 'people_list'

	#person_class = Person()

	people_list = Person().getAll()

	person_list = []

	for item in people_list:
		name = item['name'].encode('utf-8')
		#url_name = re.sub('[^A-z]', '', item['name']).encode('utf-8')
		if "^" in name:
			name = name.replace("^", "")
		state = item['state'].encode('utf-8')
		party = item['party'].encode('utf-8')
		person_tuple = (name, state, party)
		person_list.append(person_tuple)

	context = { 'person_list': person_list }
	return render(request, template_name, context)


def person_detail(request, name):
	template_name = 'person_detail.html'

	monologues = Monologue().getMonologueSpokenBy(name)
	parties = Person().getParty(name)
	congress = Congress().getCongressSession(name)
	state = Person().getState(name)

	friends_list = []
	for party in parties:
		party_members = Party().getPartyMembers(party)
		for member in party_members:
			if member['name'] == name:
				continue
			friends_list.append(member['name'].encode('utf-8'))

	random_friends = []
	if len(friends_list) <= 6:
		random_friends = friends_list
	else:
		counter = 0
		while counter < 6:
			try:
				random_friend = random.randint(0,len(friends_list))
				random_friends.append(friends_list[random_friend])
			except IndexError:
				pass
			counter = counter + 1

	monologue_list = []

	profile = {}

	#TODO
	# fix sort, sort by date and sequence

	for monologue_text, monologue_id in monologues:
		monologue_dict = {}
		date, house, session, text, sequence = monologue_id.split("-")

		#monologue = Monologue().getMonologueById(monologue_id[0].encode('utf-8'))

		#monologue_dict['date'] = date.encode('utf-8')
		#monologue_dict['house'] = house.encode('utf-8')
		#monologue_dict['session'] = session.encode('utf-8')
		#monologue_dict['sequence'] = sequence.encode('utf-8')
		#monologue_dict['monologue'] = monologue_text
		monologue_tuple = (monologue_text, monologue_id, date)
		monologue_list.append(monologue_tuple)
		#monologue_list.append(monologue_id)
		#monologue_list.append(date)

	state_list = list(set([states[0].encode('utf-8') for states in state]))
	congress_list = list(set([congress_session[0].encode('utf-8') for congress_session in congress]))
	party_list = list(set([party[0].encode('utf-8') for party in parties]))

	profile['name'] = name
	profile['sessions'] = congress_list
	profile['party'] = party_list
	profile['state'] = state_list
	profile['monologues'] = monologue_list
	profile['wiki_link'] = ''
	profile['image'] = ''
	profile['state_image'] = ''
	profile['friends_list'] = friends_list
	profile['random_friends'] = random_friends

	context = {'profile': profile}
	return render(request, template_name, context)

def state_detail(request, state):
	print "Input state info here"
	return redirect(request.META['HTTP_REFERER'])

def person_friends(request, friend):
	print "Input friends info here"
	return redirect(request.META['HTTP_REFERER'])
