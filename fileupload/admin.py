#encoding: utf-8
from fileupload.models import Directory, UploadFile
from django.contrib import admin

class DirectoryAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,        {'fields': ['directory', 'password', 'allow_list']}),
    ('容量限制',  {'fields': ['file_max_size', 'total_size']}),
  ]
  pass

class UploadFileAdmin(admin.ModelAdmin):
  pass

admin.site.register(Directory, DirectoryAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
