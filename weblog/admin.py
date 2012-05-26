from weblog.models import Person, Action, Log
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
  pass

class ActionAdmin(admin.ModelAdmin):
  pass

class LogAdmin(admin.ModelAdmin):
  pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Log, LogAdmin)
