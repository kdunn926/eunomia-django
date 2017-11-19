from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = [
	url(r'^People/', include('People.urls', namespace='People')),
	url(r'^Party/', include('Party.urls', namespace='Party')),
	url(r'^Congress/', include('Congress.urls', namespace='Congress')),
	url(r'^Monologues/', include('Monologues.urls', namespace='Monologues')),
	url(r'^Financers/', include('Financers.urls', namespace='Financers')),

	url(r'^$', TemplateView.as_view(template_name='html/landing_page.html')),
	url(r'^about/$', TemplateView.as_view(template_name='html/about.html')),
	url(r'^contact/$', TemplateView.as_view(template_name='html/contact.html')),
	url(r'^developers/$', TemplateView.as_view(template_name='html/developers.html')),
	url(r'^privacy/$', TemplateView.as_view(template_name='html/privacy_policy.html')),
 	url(r'^terms/$', TemplateView.as_view(template_name='html/terms_of_use.html')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),

	url(r'^(?!People$|Party$|Congress$|Financers$|about$|contact$|developers$|privacy$|terms$).*', TemplateView.as_view(template_name='html/landing_page.html')),
]
