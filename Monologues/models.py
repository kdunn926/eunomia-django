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
        print 'NodeHandle for node %d' % self.node()['id']
        return 'NodeHandle for node %d' % self.node()['id']

    def node(self):
        return db.get_node(self.id, self.__class__.__name__)

class Monologue(NodeHandle):

    def getMonologuesFor(self, name):
        ''' returns the ID for a given monologue '''
        monolouges = db.getMonologuesFor(name)
        return monolouges

    def getMonologueById(self, id):
        ''' returns the text for a given monologue '''
        monologue_text = db.getMonologueById(id)
        return monologue_text[0][0]

    def getMonologueSpokenBy(self, name):
        monologue_text_and_id = db.getMonologueSpokenBy(name)
        return monologue_text_and_id

    def getMonloguesByDate(self, date):
        monolouges = db.getMonloguesByDate(date)
        return monolouges
