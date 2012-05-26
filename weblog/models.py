from django.db import models

class Person(models.Model):
  name = models.CharField(max_length=200)
  money = models.DecimalField(max_digits=10, decimal_places=3)
  
  def __unicode__(self):
    return self.name

class Action(models.Model):
  name = models.CharField(max_length=100)

  def __unicode__(self):
    return self.name

class Log(models.Model):
  action = models.ForeignKey(Action)
  people = models.ManyToManyField(Person)
  content = models.CharField(max_length=1000)
  remarks = models.TextField()
  date = models.DateTimeField(auto_now=True, auto_now_add=True)
  def __unicode__(self):
    return self.content
