# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from models import Person, Action, Log

def index(request):
  return render_to_response("weblog/index.html")

class LogInfo():
  def __init__(self, l):
    self.people = list(l.people.all())
    self.action = l.action
    self.content = l.content
    self.ramarks = l.remarks
    self.date = l.date

def LogsToLogInfo(logs):
  log_info = []
  for log in logs:
    log_info.append(LogInfo(log))
  return log_info

def view_all(request):
  return render_to_response("weblog/showlog.html", 
                            {'logs': LogsToLogInfo(Log.objects.all()),})

def view_person(request, *arg, **args):
  return render_to_response("weblog/showlog.html")

def view_action(request, *arg, **args):
  return render_to_response("weblog/showlog.html")
