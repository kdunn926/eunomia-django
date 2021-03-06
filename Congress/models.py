# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from CongressionalRecord import db

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

class Congress(NodeHandle):

    def getAll(self):
        congress = db.getSingleNodeByLabel("Congress")
        return congress

    #def getSingle(self):
    #    pass

    def getCongressSession(self, name):
    	query = " MATCH (n:Person)-[r:`SPOKE`]->(monologue) WHERE n.name =~'%s' RETURN monologue.congressionalYear" % (name)
        with manager.read as r:
            result = r.execute(query, name=name).fetchall()
            r.connection.rollback()
            return result

    def getDatesForCongressNumber(self, number):
        query = """
        MATCH (m:Monologue)-[r:`PART OF`]->(c:Congress {id:  'Congress %s'})
        RETURN DISTINCT m.date ORDER BY m.date DESC
        """ % number
        with manager.read as r:
            tuple_dates = r.execute(query, number=number).fetchall()
            r.connection.rollback()

            # There is only 1 date returned for each tuple, so break apart tuple
        dates = [date[0] for date in tuple_dates]
        return dates
        # tuple_dates = db.query(query)
        # dates = [date[0] for date in tuple_dates]
        # return dates

