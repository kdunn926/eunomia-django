# -*- coding: utf-8 -*-
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

class Party(NodeHandle):

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
