# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from models import Person, Action, Log

def index(request):
  return render_to_response("weblog/index.html")

class LogInfo():
  def __init__(self, l):
    self.ID = l.id
    self.people = list(l.people.all())
    self.action = l.action
    self.content = l.content
    self.remarks = len(l.remarks) <> 0
    self.date = l.date

def LogsToLogInfo(logs):
  log_info = []
  for log in logs:
    log_info.append(LogInfo(log))
  log_info.sort(key=lambda l: l.date, reverse=True)
  return log_info

def view_all(request):
  return render_to_response("weblog/showlog.html", 
                            {'logs': LogsToLogInfo(Log.objects.all()),})

def view_person(request, *arg, **args):
  return render_to_response("weblog/showlog.html")

def view_action(request, *arg, **args):
  return render_to_response("weblog/showlog.html")
