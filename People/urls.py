from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [

	url(r'^$', views.index, name='people_index'),
	url(r'^Party$', views.PartyListView.as_view(), name='party_index'),

	#url(r'^(?P<pk>[0-9]+)/$', views.ReservationDetailView.as_view(), name = 'reservation_detail'),
	#url(r'^(?P<reservationid>[0-9]+)/edit/$', views.reservation_edit, name='reservation_edit'),
	#url(r'^add/(?P<pk>[0-9]+)?/$', views.reservation_add, name='reservation_add'),

	# catch all redirect, PUT LAST
   # url(r'^.*$', RedirectView.as_view(pattern_name='Reservations:reservation_index', permanent=False))
]
