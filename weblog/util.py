#encoding: utf-8
from models import Log, Person, Action
class LogInfo():
  def __init__(self, l, full_remarks=False):
    self.ID = l.id
    self.people = list(l.people.all())
    self.action_id = l.action_id
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

def change_money(people, money, action):
  for person in people:
    person.money += money
    person.save()

  assert action and action <> ''
  try:
    a = Action.objects.get(name=action)
  except:
    a = Action(name=action)
    a.save()

  if len(people) == 1:
    content = "{0}元".format(money)
  else:
    content = "每人{0:.3f}元".format(money)
  log = Log(action=a, content=content)
  log.save()
  for person in people:
    log.people.add(person)
  log.save()

