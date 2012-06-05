#encoding: utf-8
from django.db import models
import random
from django.utils.hashcompat import md5_constructor, sha_constructor
from django.utils.encoding import smart_str
from django.utils.crypto import constant_time_compare

def check_password(raw_password, enc_password):
  try:
    algo, salt, hsh = enc_password.split('$')
  except ValueError:
    return False
  return constant_time_compare(hsh, get_hexdigest(algo, salt, raw_password))

def get_hexdigest(algorithm, salt, raw_password):
  """
  Returns a string of the hexdigest of the given plaintext password and salt
  using the given algorithm ('md5', 'sha1' or 'crypt').
  """
  raw_password, salt = smart_str(raw_password), smart_str(salt)
  if algorithm == 'crypt':
    try:
      import crypt
    except ImportError:
      raise ValueError('"crypt" password algorithm not supported in this environment')
    return crypt.crypt(raw_password, salt)

  if algorithm == 'md5':
    return md5_constructor(salt + raw_password).hexdigest()
  elif algorithm == 'sha1':
    return sha_constructor(salt + raw_password).hexdigest()
  raise ValueError("Got unknown password algorithm type in password.")

class Directory(models.Model):
  directory = models.CharField(max_length=100, verbose_name='文件夹名称', 
    help_text='用于将上传文件分类,还可以根据需要限制容量')
  password = models.CharField(max_length=100, verbose_name='上传密码',
    help_text='必须输入正确的密码,才能允许上传,<br />注意:<br />' \
            + '1.下载时不需要密码<br />'\
            + '2.如果要修改密码,直接替换原来的内容,保存时会自动加密')
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

  def set_password(self, raw_password):
    if raw_password is None:
      self.password = '!'
    else:
      algo = 'sha1'
      a = random.random()
      b = str(a)
      c = get_hexdigest(algo, str(a), b)
      d = c[:5]
      salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
      hsh = get_hexdigest(algo, salt, raw_password)
      self.password = '%s$%s$%s' % (algo, salt, hsh)

  def check_password(self, raw_password):
    return check_password(raw_password, self.password)

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

