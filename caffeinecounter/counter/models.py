from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Counter(models.Model):
    count = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.date

class Countable(models.Model):
    type = models.ForeignKey(Type)
    counter = models.ForeignKey(Counter)

    def __unicode__(self):
        return self.name
