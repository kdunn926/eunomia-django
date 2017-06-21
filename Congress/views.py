# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Congress

def congress_detail_view(request, number):
	"""docstring for PartyList"""

	template_name = 'congress_dates.html'
	context_object_name = 'congress'

	context = {}

	#congress_dates = []
	congress_dates = Congress().getDatesForCongressNumber(number)

	context = {'congress_dates': congress_dates, 'congress_number':number}

	return render(request, template_name, context)

# Create your views here.
