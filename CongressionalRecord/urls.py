from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^People/', include('People.urls', namespace='People')),
	url(r'^Party/', include('Party.urls', namespace='Party')),
	url(r'^Congress/', include('Congress.urls', namespace='Congress')),
	url(r'^Monologues/', include('Monologues.urls', namespace='Monologues')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
]
