#encoding: utf-8
from fileupload.models import Directory, UploadFile
from django.contrib import admin
import datetime

class DirectoryAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,        {'fields': ['directory', 'password', 'allow_list']}),
    ('容量限制',  {'fields': ['file_max_size', 'total_size']}),
  ]
  pass

class UploadFileAdmin(admin.ModelAdmin):
  readonly_fields = ('directory', 'save_path', 'file_size', 'file_space', 'download_count', 'upload_date')
  fieldsets = (
    (None, { 'fields': ('file_name', 'content_type', 'description', 'auto_delete_days'),}),
    ( 'Info', { 
        'fields': (
          'directory', 'save_path', 'file_size', 'file_space', 
          'download_count', 'upload_date'), 
        'classes': ['collapse'],
#        'classes': ['wide', 'extrapretty'],
      }
    ),
  )
  list_display = ('id', 'directory', 'file_name', 'file_size', 'download_count',
                 'is_expired', 'file_type')
  def is_expired(self, obj):
    return obj.auto_delete_days > 0 and obj.upload_date + datetime.timedelta(
      days=obj.auto_delete_days) < datetime.datetime.now()
  is_expired.short_description = 'Expired'

  def file_type(self, obj):
    return obj.content_type
  file_type.short_description = 'Type'

  list_display_links = ('id', 'directory',)
  list_editable = ('file_name',)

admin.site.register(Directory, DirectoryAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
