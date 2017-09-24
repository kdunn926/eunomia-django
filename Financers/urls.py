from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from . import views

app_name = 'Congress'

urlpatterns = [

	url(r'^(?P<name>.*)/$', views.financer_detail, name='financer_detail'),
	url(r'^(?P<name>.*)/contributions/$', views.finaner_contributions, name='finaner_contributions'),

	#url(r'^Congress$', views.congress_list_index, name='congress_index'),
	#url(r'^Party/(?P<name>.*)/$', views.party_detail, name='party_index'),
	#url(r'^Party/(?P<name>.*)/members/$', views.party_members, name='party_members'),

	# catch all redirect, PUT LAST
   # url(r'^.*$', RedirectView.as_view(pattern_name='Reservations:reservation_index', permanent=False))
]
