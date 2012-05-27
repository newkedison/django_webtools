# Create your views here.
#encoding: utf-8
from django.shortcuts import render_to_response, get_object_or_404
from models import Person, Action, Log

def index(request):
  return render_to_response("weblog/index.html")

class LogInfo():
  def __init__(self, l, full_remarks=False):
    self.ID = l.id
    self.people = list(l.people.all())
    self.action = l.action
    self.content = l.content
    if not full_remarks:
      self.has_remarks = len(l.remarks) <> 0
      if self.has_remarks:
        self.remarks = u"备注信息：\n"
        if len(l.remarks) > 100:
          self.remarks += l.remarks[:100] + u"\n点击链接查看更多备注"
        else:
          self.remarks += l.remarks
    else:
      self.remarks = l.remarks
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

def view_remarks(request, *arg, **args):
  remarks = '没有备注信息'
  if 'id' in args:
    log = Log.objects.filter(id=args['id'])
    if len(log) == 1:
      loginfo = LogInfo(log[0], True)
  return render_to_response("weblog/showremarks.html", {'log': loginfo,})
