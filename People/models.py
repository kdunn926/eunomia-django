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

class Person(NodeHandle):

    def getAll(self):
        query = """
        MATCH (p:Person)
        RETURN p.name, p.state, p.party
        """
        with manager.read as r:
            result = [{'name': p[0], 'state': p[1], 'party': p[2]} for p in r.execute(query).fetchall()]
            r.connection.rollback()
            return result

    def getParty(self, name):
        query = 'MATCH (p:Person) WHERE p.name =~ "%s" RETURN p.party' % (name)
        with manager.read as r:
            result = r.execute(query).fetchall()
            r.connection.rollback()
            return result

    def getState(self, name):
        query = 'MATCH (p:Person) WHERE p.name =~"%s" RETURN p.state' % (name)
        with manager.read as r:
            result = r.execute(query).fetchall()
            r.connection.rollback()
            return result

    def getCampaignFinancers(self, name):
        query = '''
        MATCH (:Committee)-[o:CONTRIBUTED_TO]-(to:Candidate) WHERE to.candidate_name =~ '%s'
        RETURN distinct o.recipient_or_payee, o.transaction_amount
        order by toFloat(o.transaction_amount) desc
        ''' % (name+'.*')
        with manager.read as r:
            result = r.execute(query).fetchall()
            r.connection.rollback()
            return result
