#encoding: utf-8
from models import Person
from django import forms
from decimal import Decimal
from django.contrib.admin.widgets import FilteredSelectMultiple

class MoneyForm(forms.Form):
  people = forms.MultipleChoiceField(label="选择账户", 
    widget=forms.CheckboxSelectMultiple, 
    help_text="请选择要操作的账户,可以同时选中多个账户")
  p = Person.objects.all()
  people.choices = ()
  for person in p:
    people.choices.append((person.id, person.name))
  action = forms.ChoiceField(choices=(
    ('', '请选择一种操作'),
    ('add', '充值'),
    ('sub', '扣除'),
    ('suball', '购买'),
    ('addall', '返奖'),
  ),
    help_text="操作说明:<br />" \
      + "1. 充值:为每个选中的账户增加指定的金额<br />" \
      + "2. 扣除:为每个选中的账户扣除指定的金额(用于修正误操作)<br />" \
      + "3. 购买:下面的金额为总金额,所有选中账户平均扣除<br />" \
      + "4. 返奖:下面的金额为总金额,所有选中账户平均分配",
    label="操作"
  )
  money = forms.DecimalField(label="操作金额", min_value=Decimal(0), 
                   max_value = Decimal(1000), max_digits=10, decimal_places=3)
