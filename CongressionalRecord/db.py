from neo4j import contextmanager
from re import escape
from django.conf import settings

manager = contextmanager.Neo4jDBConnectionManager(settings.NEO4J_RESOURCE_URI, 
                                                  settings.NEO4J_USERNAME,
                                                  settings.NEO4J_PASSWORD)


def getNode(id, label):
    q = 'MATCH (n:{label} { id: {id} }) RETURN n'
    try:
        with manager.read as r:
            for n in r.execute(q, label=label, id=id).fetchone():
                return n
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
        return r.execute(q, l=label, k=key, value=value).fetchone()


def wildcardSearch(search_string):
    search_string = '(?i).*%s.*' % escape(search_string)
    q = """
        MATCH (m:Movie) WHERE m.title =~ {search_string} WITH collect(m) as movies
        MATCH (p:Person) WHERE p.name =~ {search_string} WITH movies, collect(p) as persons
        RETURN movies, persons
        """
    with manager.read as r:
        return r.execute(q, search_string=search_string).fetchone()

def getPeople():
    q = """
        MATCH (p:Person)
        RETURN p.name, p.state, p.party
        LIMIT 25
        """
    with manager.read as r:
        return [{'name': p[0], 'state': p[1], 'party': p[2]} for p in r.execute(q).fetchall()]

def getMonologeById(id):
    q = """
        MATCH (n:Monologue {id: {id}})<-[r:`SPOKE`]-(person)
        RETURN n.text
        """
    with manager.read as r:
        return r.execute(q, id=id).fetchall()


def getMonologuesFor(name):
    q = """
        MATCH (n:Person {name: {name}})-[r:`SPOKE`]->(monologue)
        RETURN monologue.id
        """
    with manager.read as r:
        return r.execute(q, name=name).fetchall()


def getProperNounMentions(mentioner):
    q = """
        MATCH (n:Person {name: {name}})-[r:`MENTIONED PROPER NOUN`]->(p)
        RETURN p.phrase
        """
    with manager.read as r:
        return r.execute(q, name=mentioner).fetchall()


def getMentionersOf(name):
    q = """
        MATCH (p:Person {name: {name}})<-[r:`MENTIONED`]-(person)
        RETURN person.name
        """
    with manager.read as r:
        return r.execute(q, name=name).fetchall()
