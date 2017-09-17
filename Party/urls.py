from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [


	url(r'^$', views.party_list_view, name='party_index'),
	url(r'^(?P<name>(\w+(\s+\w+\s+\w+)?))/$', views.party_detail, name='party_detail'),
	url(r'^(?P<name>(\w+\s?)+)/members/$', views.party_members, name='party_members'),
	#url(r'^(?P<name>(\w+\s?)+)/$', views.party_detail, name='party_index'),
	#url(r'^(?P<name>(\w+\s?)+)/members/$', views.party_members, name='party_members'),

	# catch all redirect, PUT LAST
   # url(r'^.*$', RedirectView.as_view(pattern_name='Reservations:reservation_index', permanent=False))
]
