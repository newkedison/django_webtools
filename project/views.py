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
  def __init__(self, x, y, length, color, name, parent_name):
    self.x = x
    self.y = y
    self.length = length
    self.color = color
    self.name = name
    self.parent_name = parent_name

class ProjectInfo():
  def __init__(self, name, description, bar_color, full_length, text_x, 
               text_length, text_font_size, line_space):
    self.name = name
    self.description = description
    self.bar_color = bar_color
    self.full_length = full_length
    self.text_x = text_x
    self.text_length = text_length
    self.text_font_size = text_font_size
    self.line_space = line_space
 
class SVGInfo():
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

def get_project(project_name):
  try:
    prj = Project.objects.get(name=project_name)
  except Project.DoesNotExist:
    return None
  return prj

def get_tasks(_project_id):
  try:
    tasks = Task.objects.filter(project_id=_project_id)
  except Task.DoesNotExist:
    return None
  return list(tasks)

class CompareError(Exception):
  def __init__(self, type_name):
    self.msg = "this two " + type_name + " cannot compare"
  def __str__(self):
    return self.msg

def compare_task(task1, task2):
  if not task1 or not task2 or (task1.parent_id <> task2.parent_id) or (task1.project_id <> task2.project_id):
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
  bar_info = []
  if prj:
    tasks = sort_tasks(get_tasks(prj.id))
    if tasks:
      prj_info = ProjectInfo(prj.name, prj.description, prj.bar_color, 
                            prj.full_length, prj.text_x, prj.text_length,
                            prj.text_font_size, prj.line_space)
      all_time = (prj.end_date - prj.begin_date).total_seconds()
      all_len = prj_info.full_length
      y = 10
      time_to_len = all_len / all_time
      x = prj_info.text_x + prj_info.text_length
      _bar = Bar(x, y, all_len, prj_info.bar_color, prj_info.name, "")
      bar_info.append(_bar)
      y += prj_info.line_space
      for task in tasks:
        toggle_name = "bar_" + str(task.id)
        parent_name = task.parent_id and \
            "bar_" + str(task.parent_id.id) or prj_info.name
        _bar = Bar(time_len(prj.begin_date, task.begin_date, time_to_len) + x,
                  y, time_len(task.begin_date, task.end_date, time_to_len),
                  task.bar_color, toggle_name, parent_name)
        y += prj_info.line_space
        bar_info.append(_bar)
      svg = SVGInfo(0, 0, x + all_len + 100, 
                    len(tasks) * (prj_info.line_space) + 100)
      return svg, prj_info, bar_info

  return None

def view_project(r):
  svg, prj, bar = get_sorted_bar("aaa")
  return render_to_response("project/view.html", {'bars': bar, 
                                                  'prj': prj,
                                                  'svg': svg,})

