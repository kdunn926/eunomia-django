# Create your views here.
from django.shortcuts import render, redirect
from django.views import generic

from Financers.models import Financers

import re
import random

def financer_detail(request, name):
	template_name = 'financer_detail.html'

	financer = ''
	if name != "Unknown":
		name = name.replace(',', '')
		financer = Financers().getFinancersContributions(name)
	profile = {}
	print financer
	profile['name'] = name

	context = {'profile': profile}
	return render(request, template_name, context)

def finaner_contributions(request, name):
	template_name = 'financer_contributions.html'

	print name

	candidates = Financers().getFinancersContributions(name)

	print candidates

	profile = {}
	profile['name'] = name
	#profile['financers_list'] = financers_list

	context = {'profile': profile}

	return render(request, template_name, context)
