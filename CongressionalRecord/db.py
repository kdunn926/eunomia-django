from neo4j import contextmanager
from neo4j import connection
from re import escape
from django.conf import settings

connection.http.REQUEST_TIMEOUT = 9999
manager = contextmanager.Neo4jDBConnectionManager(settings.NEO4J_RESOURCE_URI,
                                                  settings.NEO4J_USERNAME,
                                                  settings.NEO4J_PASSWORD)
def query(query, executor=''):
    try:
        with manager.read as r:
            result = r.execute(query).fetchall()
            r.connection.rollback()
            return result
    except IndexError:
        return {}

def getNode(id, label):
    q = 'MATCH (n:{label} { id: {id} }) RETURN n'
    try:
        with manager.read as r:
            for n in r.execute(q, label=label, id=id).fetchone():
                r.connection.rollback()
                return n
    except IndexError:
        return {}

def getSingleNodeByLabel(label_string):
    q = 'MATCH (n:%s) RETURN n' % label_string
    try:
        with manager.read as r:
            result = r.execute(q, label=label_string)
            return result
    except IndexError:
        return {}

"""
def deleteNode(id, label):
    q = '''
        MATCH (n:%s { id: {id} })
        OPTIONAL MATCH (n)-[r]-()
        DELETE n, r
        ''' % label
    with manager.transaction as w:
        w.execute(q, id=id)
""";

def getUniqueNode(label, key, value):
    q = 'MATCH (n:{l} { {k}: {value} }) RETURN n LIMIT 1'
    with manager.read as r:
        result = r.execute(q, l=label, k=key, value=value).fetchone()
        r.connection.rollback()
        return result


def wildcardSearch(search_string):
    search_string = '(?i).*%s.*' % escape(search_string)
    q = """
        MATCH (m:Movie) WHERE m.title =~ {search_string} WITH collect(m) as movies
        MATCH (p:Person) WHERE p.name =~ {search_string} WITH movies, collect(p) as persons
        RETURN movies, persons
        """
    with manager.read as r:
        result = r.execute(q, search_string=search_string).fetchone()
        r.connection.rollback()
        return result

def getPeople():
    q = """
        MATCH (p:Person)
        RETURN p.name, p.state, p.party
        """
    with manager.read as r:
        result = [{'name': p[0], 'state': p[1], 'party': p[2]} for p in r.execute(q).fetchall()]
        r.connection.rollback()
        return result

def getState(name):
    q = 'MATCH (p:Person) WHERE p.name =~"%s" RETURN p.state' % (name)
    with manager.read as r:
        result = r.execute(q).fetchall()
        r.connection.rollback()
        return result

def getAllParties():
    q = """
        MATCH (p:Party)
        RETURN p
        """
    with manager.read as r:
        result = r.execute(q).fetchall()
        r.connection.rollback()
        return result

def getParty(name):
    q = 'MATCH (p:Person) WHERE p.name =~ "%s" RETURN p.party' % (name)
    with manager.read as r:
        result = r.execute(q).fetchall()
        r.connection.rollback()
        return result

def getPartyMembers(name):
    q = 'MATCH (n:Person) WHERE n.party = "%s" RETURN n.name, n.state' % (name)
    with manager.read as r:
        result = [{'name': n[0], 'state': n[1]} for n in r.execute(q).fetchall()]
        r.connection.rollback()
        return result

def getMonologueById(id):
    q = """
        MATCH (n:Monologue {id: {id}})
        RETURN n """#, n.date, n.wordHistogram, n.properNouns, n.speaker, n.crongressionalYear, n.text, n.numWords, n.wordSet, n.branch, n.party
        #"""
    with manager.read as r:
        monologue = r.execute(q, id=id).fetchall()
        r.connection.rollback()
        return monologue

def getMonologueSpokenBy(name):
    q = """
        MATCH (n:Person {name: {name}})-[r:`SPOKE`]->(monologue)
        WHERE NOT monologue.text STARTS WITH ' H.'
        AND NOT monologue.text STARTS WITH '[[P' AND NOT monologue.text STARTS WITH ' [[P'
        AND length(monologue.text) > 1
        RETURN monologue.text, monologue.id ORDER BY monologue.id DESC
        """
    with manager.read as r:
        result = r.execute(q, name=name).fetchall()
        r.connection.rollback()
        return result

def getMonologueID(name):
    q = """
        MATCH (n:Person {name: {name}})-[r:`SPOKE`]->(monologue)
        RETURN monologue.id
        """
    with manager.read as r:
        result = r.execute(q, name=name).fetchall()
        r.connection.rollback()
        return result

def getCongressByName(name):
    q = " MATCH (n:Person)-[r:`SPOKE`]->(monologue) WHERE n.name =~'%s' RETURN monologue.congressionalYear" % (name)
    with manager.read as r:
        result = r.execute(q, name=name).fetchall()
        r.connection.rollback()
        return result

def getMonloguesByDate(year):
    q = """ MATCH (m:Monologue) WHERE m.date='%s' RETURN DISTINCT m ORDER BY m.date DESC""" % (year)
    with manager.read as r:
        result = r.execute(q).fetchall()
        r.connection.rollback()
        return result

def getDatesForCongressNumber(number):
    q = """
        MATCH (m:Monologue)-[r:`PART OF`]->(c:Congress {id:  {number}})
        RETURN DISTINCT m.date ORDER BY m.date DESC
      """
    with manager.read as r:
        result = r.execute(q, number="Congress "+number).fetchall()
        r.connection.rollback()
        return result

def getProperNounMentions(mentioner):
    q = """
        MATCH (n:Person {name: {name}})-[r:`MENTIONED PROPER NOUN`]->(p)
        RETURN p.phrase
        """
    with manager.read as r:
        result = r.execute(q, name=mentioner).fetchall()
        r.connection.rollback()
        return result

def getMentionersOf(name):
    q = """
        MATCH (p:Person {name: {name}})<-[r:`MENTIONED`]-(person)
        RETURN person.name
        """
    with manager.read as r:
        result = r.execute(q, name=name).fetchall()
        r.connection.rollback()
        return result

def getCampaignFinancers(name):

    q = '''
        MATCH (:Committee)-[o:CONTRIBUTED_TO]-(to:Candidate {candidate_name: {name}})
        RETURN distinct o.recipient_or_payee, o.transaction_amount
        order by toFloat(o.transaction_amount) desc
        '''
    with manager.read as r:
        result = r.execute(q, name=name).fetchall()
        r.connection.rollback()
        return result
