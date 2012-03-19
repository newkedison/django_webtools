from django.db import models

class Project(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=10000)
  view_password = models.CharField(max_length=20, blank=True)
  begin_date = models.DateField()
  end_date = models.DateField()
  bar_color = models.CharField(max_length=15)
  full_length = models.IntegerField(default=800)
  text_x = models.IntegerField(default=10)
  text_length = models.IntegerField(default=40)
  text_font_size = models.IntegerField(default=10)
  line_space = models.IntegerField(default=30)
  def __unicode__(self):
    return self.name

class Task(models.Model):
  project_id = models.ForeignKey(Project)
  parent_id = models.ForeignKey('self', blank=True, null=True)
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=10000)
  begin_date = models.DateField()
  end_date = models.DateField()
  bar_color = models.CharField(max_length=15)
  def __unicode__(self):
    return self.name

class CheckPoint(models.Model):
  task_id = models.ForeignKey(Task)
  date = models.DateField()
  description = models.CharField(max_length=10000)
  def __unicode__(self):
    return description

class MileStone(models.Model):
  project_id = models.ForeignKey(Project)
  date = models.DateField()
  description = models.CharField(max_length=10000)
  def __unicode__(self):
    return description

