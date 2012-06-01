#encoding: utf-8
from django.db import models

class Directory(models.Model):
  directory = models.CharField(max_length=100, verbose_name='保存路径', 
    help_text='用于将上传文件分类,还可以根据需要限制容量')
  password = models.CharField(max_length=100, verbose_name='上传密码',
    help_text='必须输入正确的密码,才能允许上传,注意,下载时不需要密码')
  file_max_size = models.IntegerField(default=100, 
    verbose_name='最大文件大小(单位:MB)',
    help_text='上传的文件不允许超过此大小, 注意:此数值不能超过100MB')
  total_size = models.IntegerField(default=1024, 
    verbose_name='容量上限(单位:MB)',
    help_text='所有上传文件总大小限制,以4KB为最小单位,不足4KB部分按4KB算')
  used_size = models.IntegerField(editable=False, default=0)
  allow_list = models.BooleanField(default=True, verbose_name='允许列出文件',
    help_text='是否允许列出此文件夹下的所有文件,以供下载')
  
  def __unicode__(self):
    return self.directory

class UploadFile(models.Model):
  directory = models.ForeignKey(Directory)
  file_name = models.CharField(max_length=100)
  content_type = models.CharField(max_length=30)
  save_path = models.CharField(editable=False, max_length=1000)
  file_size = models.IntegerField(editable=False)
  file_space = models.IntegerField(editable=False)
  download_count = models.IntegerField(editable=False)
  upload_date = models.DateTimeField(auto_now_add=True)
  description = models.TextField(blank=True)
  auto_delete_days = models.IntegerField(default=0)

  def __unicode__(self):
    return self.file_name

