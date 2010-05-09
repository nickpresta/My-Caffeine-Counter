from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

class Counter(models.Model):
    count = models.IntegerField()
    date = models.DateField(auto_now_add=True, unique_for_date=True)

    def __unicode__(self):
        return self.date.strftime("%Y-%m-%d %I:%M:%S %p %Z")

class Countable(models.Model):
    type = models.ForeignKey(Type)
    counter = models.ForeignKey(Counter)

    def __unicode__(self):
        return self.type.name
