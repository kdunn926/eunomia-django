from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [


	#url(r'^Monologues$', views.monologue_list_index, name='monologue_index'),
	#url(r'^Party/(?P<name>.*)/$', views.party_detail, name='party_index'),
	#url(r'^Party/(?P<name>.*)/members/$', views.party_members, name='party_members'),

	# catch all redirect, PUT LAST
   # url(r'^.*$', RedirectView.as_view(pattern_name='Reservations:reservation_index', permanent=False))
]
