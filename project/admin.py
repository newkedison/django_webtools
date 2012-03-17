from project.models import Project, Task, CheckPoint, MileStone
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
  pass

class TaskAdmin(admin.ModelAdmin):
  pass

class CheckPointAdmin(admin.ModelAdmin):
  pass

class MileStoneAdmin(admin.ModelAdmin):
  pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(CheckPoint, CheckPointAdmin)
admin.site.register(MileStone, MileStoneAdmin)
