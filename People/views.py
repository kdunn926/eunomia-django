# Create your views here.
from django.shortcuts import render, redirect

from .models import Person
from Congress.models import Congress
from Party.models import Party
from Monologues.models import Monologue

import re
import random

def index(request):
	template_name = 'people_index.html'
	context_object_name = 'people_list'

	people_list = Person().getAll()

	person_list = []

	for item in people_list:
		name = item['name'].encode('utf-8')
		name = name.replace("^", "").replace(":", "").replace("(", "").replace(")", "").replace("'", "")

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

	# Campaign finance data has name in the format of LASTNAME, FIRSTNAME MIDDLE
	#  So re-arrange the given name here for future finance data request
	split_name = name.replace(".", "").split(" ")#, 1)[1].upper() + ", " + name.split(" ", 1)[0].upper()

	if len(split_name) == 2:
		campaign_name = name.split(" ", 1)[1].upper() + ", " + name.split(" ", 1)[0].upper()
	elif len(split_name) == 3:
		campaign_name = split_name[-1].upper() + ", " + split_name[0].upper()
	else:
		print split_name
		campaign_name = ""

	campaign_financers = Person().getCampaignFinancers(campaign_name)

	financers_list = []
	for financer in campaign_financers:
		contributor = financer[0]
		amount = financer[1]
		if contributor is None:
			contributor = "Unknown"
		financers_list.append((contributor, amount))

	top_financers_list = financers_list[:10]

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

	if congress_list:
		profile['sessions'] = congress_list
	else:
		profile['sessions'] = [0]

	if party_list:
		profile['party'] = party_list
	else:
		profile['party'] = ['Uknown']

	if state_list:
		profile['state'] = state_list
	else:
		profile['state'] = ['Uknown']

	if monologue_list:
		profile['monologues'] = monologue_list
	else:
		profile['monologues'] = []

	if campaign_financers:
		profile['financers'] = financers_list
	else:
		profile['financers'] = []

	if top_financers_list:
		profile['top_financers'] = top_financers_list
	else:
		profile['top_financers'] = []

	profile['wiki_link'] = ''
	profile['image'] = ''
	profile['state_image'] = ''

	if friends_list:
		profile['friends_list'] = friends_list
	else:
		profile['friends_list'] = []

	if random_friends:
		profile['random_friends'] = random_friends
	else:
		profile['random_friends'] = []

	context = {'profile': profile}
	return render(request, template_name, context)

def state_detail(request, state):

	return redirect(request.META['HTTP_REFERER'])

def person_financers(request, name):
	template_name = 'person_financers.html'

	# Campaign finance data has name in the format of LASTNAME, FIRSTNAME MIDDLE
	#  So re-arrange the given name here for future finance data request
	split_name = name.replace(".", "").split(" ")#, 1)[1].upper() + ", " + name.split(" ", 1)[0].upper()

	if len(split_name) == 2:
		campaign_name = name.split(" ", 1)[1].upper() + ", " + name.split(" ", 1)[0].upper()
	elif len(split_name) == 3:
		campaign_name = split_name[-1].upper() + ", " + split_name[0].upper()
	else:
		print split_name
		campaign_name = ""

	campaign_financers = Person().getCampaignFinancers(campaign_name)

	financers_list = []
	for financer in campaign_financers:

		contributor = financer[0]
		amount = financer[1]
		if contributor is None:
			contributor = "Unknown"
		financers_list.append((contributor, amount))
	top_financers_list = financers_list[:10]

	profile = {}
	profile['name'] = name
	profile['financers_list'] = financers_list

	context = {'profile': profile}

	return render(request, template_name, context)
