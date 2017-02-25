# Create your views here.
from django.shortcuts import render
from django.views import generic

from .models import Person, Party
from CongressionalRecord import db

class PeopleListView(generic.ListView):
    template_name = 'people_index.html'
    context_object_name = 'people_list'
    model = Person

def index(request):
    template_name = 'people_index.html'
    context_object_name = 'people_list'

    people_list = db.getPeople()

    context = { context_object_name: people_list }
    return render(request, template_name, context)

class PartyListView(generic.ListView):
    """docstring for PartyList"""

    template_name = 'party_index.html'
    #context_object_name = 'people'
    model = Party

    def get_queryset(self):
        return Party.objects.filter()
