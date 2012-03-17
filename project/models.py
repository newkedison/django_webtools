from django.db import models

class Project(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=10000)
  view_password = models.CharField(max_length=20, blank=True)
  begin_date = models.DateTimeField()
  end_date = models.DateTimeField()
  def __unicode__(self):
    return self.name

class Task(models.Model):
  project_id = models.ForeignKey(Project)
  parent_id = models.ForeignKey('self', blank=True, null=True)
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=10000)
  begin_date = models.DateTimeField()
  end_date = models.DateTimeField()
  bar_color = models.IntegerField()
  def __unicode__(self):
    return self.name

class CheckPoint(models.Model):
  task_id = models.ForeignKey(Task)
  date = models.DateTimeField()
  description = models.CharField(max_length=10000)
  def __unicode__(self):
    return description

class MileStone(models.Model):
  project_id = models.ForeignKey(Project)
  date = models.DateTimeField()
  description = models.CharField(max_length=10000)
  def __unicode__(self):
    return description

