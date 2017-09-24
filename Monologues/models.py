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

class Monologue(NodeHandle):

    # def getMonologuesFor(self, name):
    #     ''' returns the ID for a given monologue '''
    #     monolouges = db.getMonologuesFor(name)
    #     return monolouges

    def getMonologueById(self, id):
        ''' returns the text for a given monologue '''
        query = """
        MATCH (n:Monologue {id: {id}})
        RETURN n """
        with manager.read as r:
            monologue = r.execute(query, id=id).fetchall()
            r.connection.rollback()
            return monologue[0][0]

    def getMonologueSpokenBy(self, name):
        ''' returns the monologue text and id spoken by a person '''
        query = """
        MATCH (n:Person {name: {name}})-[r:`SPOKE`]->(monologue)
        WHERE NOT monologue.text STARTS WITH ' H.'
        AND NOT monologue.text STARTS WITH '[[P' AND NOT monologue.text STARTS WITH ' [[P'
        AND length(monologue.text) > 1
        RETURN monologue.text, monologue.id ORDER BY monologue.id DESC
        """
        with manager.read as r:
            result = r.execute(query, name=name).fetchall()
            r.connection.rollback()
            return result

    def getMonloguesByDate(self, date):
        ''' returns all of the monologues for a given date '''
        query = """ MATCH (m:Monologue) WHERE m.date='%s' RETURN DISTINCT m ORDER BY m.date DESC""" % (date)
        with manager.read as r:
            result = r.execute(query).fetchall()
            #r.connection.rollback()
            return result
