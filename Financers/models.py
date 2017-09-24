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

class Financers(NodeHandle):

    def getFinanceDetails(self, name):
    	query = '''MATCH (n:Contributor {name: {name}}) RETURN n'''
        with manager.read as r:
            result = r.execute(query, name=name).fetchall()
            r.connection.rollback()
            return result

    def getFinancersContributions(self, name):
    	query = '''MATCH (c:Committee {name: {name}})-[o:CONTRIBUTED_TO]-(to:Candidate)
			RETURN distinct c.committee_name,to.candidate_name, toFloat(o.transaction_amount)
			order by toFloat(o.transaction_amount) desc'''
        with manager.read as r:
            result = r.execute(query, name=name).fetchall()
            r.connection.rollback()
            return result
