from django.db import models

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
    id = models.IntegerField(primary_key=True, null=False)

    spoke = models.CharField(max_length=200)

class Person(NodeHandle):
    #name = models.CharField(max_length=200)

    def _name(self):
        return self.node().get('name', 'Missing name')
    name = property(_name)

    #state = models.CharField(max_length=200)

    def _state(self):
        return self.node().get('state', 'Missing state')
    state = property(_state)

    #party = models.CharField(max_length=200)

    def _party(self):
        return self.node().get('party', 'Missing party')
    party = property(_party)

    # TODO relationships
    #mentioned_person = models.CharField(max_length=200)
    #spoke = models.Relationship('self', rel_type='SPOKE', preserve_ordering=True)

    def __unicode__(self):
       return str(self.name)



class Party(models.Model):
    id = models.IntegerField(primary_key=True, null=False)

    party = models.CharField(max_length=140)


class Congress(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    date = models.DateField()
