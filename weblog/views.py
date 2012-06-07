# Create your views here.
#encoding: utf-8
from django.shortcuts import render_to_response, get_object_or_404, render
from models import Person, Action, Log
from util import LogsToLogInfo, change_money
from forms import MoneyForm
from django.http import Http404, HttpResponse, HttpResponseRedirect

def index(request, *arg, **args):
  return render_to_response("weblog/index.html")

def view_all(request):
  people = request.GET.get('p', None)
  action = request.GET.get('a', None)
  if people:
    p = get_object_or_404(Person, id=people)
  if action:
    a = get_object_or_404(Action, id=action)

  if people:
    logs = p.log_set.all()
    if action:
      logs = logs.filter(action=a)
  elif action:
    logs = Log.objects.filter(action=a)
  else:
    logs = Log.objects.all()
  return render_to_response("weblog/showlog.html", 
                            {'logs': LogsToLogInfo(logs),})

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

def view_discuss(request):
  return render_to_response('weblog/discuss.html')

def view_money(request):
  p = Person.objects.all()
  return render_to_response('weblog/money.html', {'people': p,})

def money_manage(request):
  if request.method == 'POST':
    form = MoneyForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      people = []
      for p in form_data['people']:
        people.append(get_object_or_404(Person, id=p))
      
      action = form_data['action']
      money = form_data['money']
      if action == 'add':
        change_money(people, money, "充值")
      elif action == 'sub':
        change_money(people, money * -1, "扣除")
      elif action == 'addall':
        change_money(people, money / len(people), "返奖")
      elif action == 'suball':
        change_money(people, money / len(people) * -1, "购买")
      else:
        raise Http404
      return HttpResponseRedirect('../success/')
  else:
    form = MoneyForm()
  return render(request, 'weblog/money_manage.html', 
                {'form': form,
                })

def success(request):
  return render_to_response('weblog/success.html')
