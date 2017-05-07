from __future__ import unicode_literals

from django.db import models
from CongressionalRecord import db

# Create your models here.
class NodeHandle(models.Model):
    id = models.CharField(max_length=64, unique=True, editable=False, primary_key=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        print 'NodeHandle for node %d' % self.node()['id']
        return 'NodeHandle for node %d' % self.node()['id']

    def node(self):
        return db.get_node(self.id, self.__class__.__name__)

class Person(NodeHandle):

    def getAll(self):
        people = db.getPeople()
        return people

    def getSingle(self):
        pass

class Party(models.Model):

    def getAll(self):
        party = db.getAllParties()
        return party

    def getSingleByName(self, name):
        party = db.getParty(name)
        return party

    def getSingleByID(self, id):
        party = db.getNode(id, 'Party')
        return party

    def getPartyMembers(self, name):
        party = db.getPartyMembers(name)
        return party


class Congress(models.Model):

    def getAll(self):
        congress = db.getSingleNodeByLabel("Congress")
        return congress

    def getSingle(self):
        pass

