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

class Congress(NodeHandle):

    def getAll(self):
        congress = db.getSingleNodeByLabel("Congress")
        return congress

    def getSingle(self):
        pass

    def getCongressSession(self, name):
    	congress = db.getCongressByName(name)
    	return congress

