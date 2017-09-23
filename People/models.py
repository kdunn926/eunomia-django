from __future__ import unicode_literals

from django.db import models
from CongressionalRecord import db

# Create your models here.
class NodeHandle(models.Model):
    id = models.CharField(max_length=64, unique=True, editable=False, primary_key=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'NodeHandle for node %d' % self.node()['id']

    def node(self):
        return db.get_node(self.id, self.__class__.__name__)

class Person(NodeHandle):

    def getAll(self):
        people = db.getPeople()
        return people

    def getSingle(self):
        pass

    def getParty(self, name):
        party = db.getParty(name)
        return party

    def getState(self, name):
        state = db.getState(name)
        return state

    def getCampaignFinancers(self, name):
        campaign_financers = db.getCampaignFinancers(name)
        return campaign_financers
