# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from CongressionalRecord import db

from neo4j import contextmanager
from neo4j import connection
from re import escape
from django.conf import settings

connection.http.REQUEST_TIMEOUT = 9999
manager = contextmanager.Neo4jDBConnectionManager(settings.NEO4J_RESOURCE_URI,
                                                  settings.NEO4J_USERNAME,
                                                  settings.NEO4J_PASSWORD)

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
        query = """
        MATCH (p:Party)
        RETURN p
        """
        with manager.read as r:
            result = r.execute(query).fetchall()
            r.connection.rollback()
            return result

    def getSingleByName(self, name):
        query = 'MATCH (p:Person) WHERE p.name =~ "%s" RETURN p.party' % (name)
        with manager.read as r:
            result = r.execute(query).fetchall()
            r.connection.rollback()
            return result

    def getSingleByID(self, id):
        party = db.getNode(id, 'Party')
        return party

    def getPartyMembers(self, name):
        query = 'MATCH (n:Person) WHERE n.party = "%s" RETURN n.name, n.state' % (name)
        with manager.read as r:
            result = [{'name': n[0], 'state': n[1]} for n in r.execute(query).fetchall()]
            r.connection.rollback()
            return result
