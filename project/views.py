# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from models import Project, Task, CheckPoint, MileStone

def index(request):
  return render_to_response("index.html")

def test1(r):
  return render_to_response("test1.html")

def test2(r):
  return render_to_response("test2.html")

def bar(r):
  return render_to_response("bar.html")

class Bar():
  def __init__(self, x, y, length, color):
    self.x = x
    self.y = y
    self.length = length
    self.color = color
  def __expr__(self):
    return self.x + ', ' + self.y + ', ' + self.length + ', ' + self.color

def get_project(project_name):
  try:
    prj = Project.objects.get(name=project_name)
  except Project.DoesNotExist:
    return None
  return prj

def get_tasks(id):
  try:
    tasks = Task.objects.filter(project_id=id)
  except Task.DoesNotExist:
    return None
  return list(tasks)

class CompareError(Exception):
  def __init__(self, type_name):
    self.msg = "this two " + type_name + " cannot compare"
  def __str__(self):
    return self.msg

def compare_task(task1, task2):
  if not task1 or not task2 or (task1.parent_id <> tast2.parent_id) or (task1.project_id <> task2.project_id):
    raise CompareError("task")
  return cmp(task1.begin_date, task2.begin_date)

def sort_by_parent_id(tasks, parent):
  ret = []
  for task in tasks:
    if task.parent_id == parent:
      ret.append(task)
  if len(ret) == 0:
    return None
  ret.sort(compare_task)
  ret2 = []
  for task in ret:
    ret2.append(task)
    tasks.remove(task)
    sub = sort_by_parent_id(tasks, task)
    if sub:
      ret2.extend(sub)
  return ret2

def sort_tasks(tasks):
  if not tasks or len(tasks) == 0:
    return None
  return sort_by_parent_id(tasks, None)
  
def time_len(begin, end, time_to_len):
  return (end - begin).total_seconds() * time_to_len

def get_sorted_bar(project_name):
  prj = get_project(project_name)
  ret = []
  if prj:
    tasks = sort_tasks(get_tasks(prj.id))
    if tasks:
      all_time = (prj.end_date - prj.begin_date).total_seconds()
      all_len = 800
      y = 10
      time_to_len = all_len / all_time
      _bar = Bar(10, y, all_len, 0x00FF00)
      ret.append(_bar)
      y += 30
      for task in tasks:
        _bar = Bar(time_len(prj.begin_date, task.begin_date, time_to_len) + 10,
                  y, time_len(task.begin_date, task.end_date, time_to_len),
                  0x0000FF)
        y += 30
        ret.append(_bar)
      return ret

  return None

def view_project(r):
  return render_to_response("project/view.html", {'bars': get_sorted_bar("aaa") })

