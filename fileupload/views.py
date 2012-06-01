# Create your views here.
#encoding: utf-8
import os
import re
import sys #for print >> sys.stderr, 'some log'
import tempfile
import datetime
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from models import Directory, UploadFile

class UploadForm(forms.Form):
  directory = forms.CharField(label='文件夹', max_length=100, 
    help_text='文件要保存在哪一个文件夹内.注意,这个文件夹必须已存在.')
  password = forms.CharField(label='密码', max_length=100, 
    widget=forms.PasswordInput, help_text='该文件夹的上传密码')
  filename = forms.CharField(label='文件名', max_length=30, required=False,
    help_text='文件被下载时使用的文件名,不能和同文件夹内的其他已存在的文件重复'\
    + '<br />只能是字母,数字,小数点,下划线,减号.如果留空,表示使用上传的文件名'\
    + '<br />如果要使用中文文件名,可以先修改欲上传的文件为该名字,然后这里留空')
  content_type = forms.ChoiceField(label='文件类型', required=False,
    help_text='一般选择自动检测,会根据扩展名自动判断,对于一些没有扩展名的文件,'\
            + '而且需要在线查看的,才需要自行指定类型',
    choices = [
      ('', '自动检测'),
      ('text/plain', '文本文件'),
      ('text/html', 'HTML文件'),
      ('text/xml', 'XML文件'),
      ('application/pdf', 'PDF文件'),
      ('image/*', '图片文件'),
      ('video/*', '视频文件'),
      ('audio/*', '音频文件'),
      ('application/msword', 'word文件'),
      ('application/vnd.ms-excel', 'Excel文件'),
      ('application/vnd.ms-powerpoint', 'PPT文件'),
      ('application/x-javascript', 'JAVA/javascript'),
      ('application/*zip*', '压缩包'),
      ('application/octet-stream', '其他二进制文件'),
    ])
  auto_delete = forms.CharField(label='自动删除时间', initial=0,
    help_text='单位:天.达到指定天数后,该文件会自动删除,设为0表示不自动删除')
  description = forms.CharField(label='文件描述', required=False,
    help_text='对文件的描述,可以为空', widget=forms.Textarea)
  file = forms.FileField(label='待上传文件')

  def clean_filename(self):
    fn = self.cleaned_data.get('filename', '')
    if fn <> '':
      if re.match('[0-9a-zA-Z_][-0-9a-zA-Z_.]*', fn) == None:
        raise forms.ValidationError('文件名不合法(只能由数字,字母,下划线组成)')
    return fn
 
def get_save_path(file_name):
  _, filename = os.path.split(file_name)
  prefix, suffix = os.path.splitext(filename)
  path = os.path.join(os.path.dirname(__file__), 'files').encode('utf-8')
  if not os.path.exists(path):
    os.makedirs(path)
  suffix = suffix.encode('utf-8')
  prefix = prefix.encode('utf-8')
  _, filename = tempfile.mkstemp(suffix, prefix+"_", path)
  return filename

def handle_upload_file(directory, f, name, form_data):
  min_block = 4 * 1024
  size = f.size
  space = (f.size + min_block - 1) / min_block * min_block
  save_path = get_save_path(name)
  content_type = f.content_type if form_data['content_type'] == '' \
                                else form_data['content_type']
  UploadFile.objects.create(directory=directory, 
                            file_name=name,
                            content_type=content_type,
                            save_path=save_path,
                            file_size=size,
                            file_space=space,
                            download_count=0,
                            description=form_data['description'],
                            auto_delete_days=form_data['auto_delete'],
                           )
  destination = open(save_path, 'wb+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()
  directory.used_size += space
  directory.save()

def index(request, *arg, **args):
  return render_to_response('fileupload/index.html')

def upload(request):
  if request.method == 'POST':
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
      form_data = form.cleaned_data
      try:
        d = Directory.objects.get(directory=form_data['directory'])
      except:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '文件夹不存在或密码错误'})
      if d.password <> form_data['password']:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '文件夹不存在或密码错误'})
      f = request.FILES['file']
      name = form_data['filename'] if form_data['filename'] <> '' else f.name
      if UploadFile.objects.filter(directory=d, file_name=name).count() <> 0:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '该文件名已存在'})
      if f.size > d.file_max_size * 1024 * 1024:
        return render_to_response('fileupload/uploadfail.html',
                    {'error_message': '文件大小超过文件夹允许单个文件的上限'})
      check_used(d)
      if f.size + d.used_size > d.total_size * 1024 * 1024:
        return render_to_response('fileupload/uploadfail.html',
                    {'error_message': '文件夹已满'})
      try:
        handle_upload_file(d, f, name, form_data)
      except:
        return render_to_response('fileupload/uploadfail.html',
                    {'error_message': '保存文件失败'})

      return HttpResponseRedirect(
        'success/?u={0:.3f}&t={1}&d={2}&fs={3}&on={4}&nn={5}'.format(
        d.used_size / 1024.0 / 1024, d.total_size, d, f.size, 
          f.name.encode('utf-8'), name.encode('utf-8')))
    else:
      return render(request, 'fileupload/upload.html', {'form': form})
  else:
    form = UploadForm()
    return render(request, 'fileupload/upload.html', {'form': form})

def success(request):
  dir_used = request.GET.get('u', '')
  dir_total = request.GET.get('t', '')
  old_name = request.GET.get('on', '')
  new_name = request.GET.get('nn', '')
  dir_name = request.GET.get('d', '')
  file_size = request.GET.get('fs', '')

  return render_to_response('fileupload/success.html', {
    'old_name': old_name,
    'new_name': new_name,
    'dir': dir_name,
    'file_size': file_size,
    'dir_used': dir_used,
    'dir_total': dir_total,
  })

def check_used(d):
  files = UploadFile.objects.filter(directory=d)
  used_sum = 0
  import sys
  for f in files:
    if f.auto_delete_days > 0:
      upload_date = f.upload_date
      if upload_date + datetime.timedelta(days=f.auto_delete_days) \
         < datetime.datetime.now():
        print >> sys.stderr, 'remove uploaded file {0}'.format(f.save_path), \
            'uploaded when {0} and expired time is {1} days'.format(upload_date,
                                                             f.auto_delete_days)
        os.remove(f.save_path)
        f.delete()
        continue
    used_sum += f.file_space
  d.used_size = used_sum
  d.save()

class ListDirForm(forms.Form):
  directory = forms.CharField(label='要查看的文件夹名称', max_length=100)
  password = forms.CharField(label='请输入该文件的密码', max_length=100, 
                             widget=forms.PasswordInput)

def list_dir(request, *arg, **args):
  if request.method == 'POST':
    form = ListDirForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      try:
        d = Directory.objects.get(directory=form_data['directory'])
      except:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '文件夹不存在或密码错误'})
      if d.password <> form_data['password']:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '文件夹不存在或密码错误'})
      check_used(d)
      files = []
      if d.allow_list:
        files = list(UploadFile.objects.filter(directory=d))
        for f in files:
          f.file_size = '{0:.2f}'.format(f.file_size / 1024.0)
          if not ((f.content_type in ['text/plain', 'text/html', 'text/xml', 
                                    'application/pdf']) or \
             re.match('image/.*', f.content_type)):
            f.content_type = ''
      return render_to_response('fileupload/listfiles.html', {
        'dir': d,
        'dir_used': '{:.3f}'.format(d.used_size / 1024.0 / 1024),
        'files': files,
      })
  else:
    form = ListDirForm(initial={'directory': args['dir']})
    return render(request, 'fileupload/list_check.html', {
      'form': form, 
      'action': args['dir'],
    })

def download(request, *arg, **args):
  d = get_object_or_404(Directory, directory=args['dir'])
  f = get_object_or_404(UploadFile, directory=d, 
                        file_name=args['filename'])
  if not os.path.exists(f.save_path.encode('utf-8')):
    raise Http404
  wrapper = FileWrapper(file(f.save_path.encode('utf-8')))
  response = HttpResponse(wrapper, content_type=f.content_type)
  response['Content-Length'] = os.path.getsize(f.save_path.encode('utf-8'))
  x = response['Content-Length']
  if args['method'] == 'get':
    response['Content-Disposition'] = 'attachment; filename={0}'.format(f.file_name)
  return response

class DeleteConfirmForm(forms.Form):
  password = forms.CharField(label='请输入文件夹的密码', max_length=100, 
                             widget=forms.PasswordInput)

def delete(request, *arg, **args):
  if args['dir'] == '' or args['file_id'] == '':
    raise Http404
  if request.method == 'POST':
    form = DeleteConfirmForm(request.POST)
    if form.is_valid():
      pwd = form.cleaned_data['password']
      try:
        d = Directory.objects.get(directory=args['dir'])
      except:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '文件夹不存在或密码错误'})
      if d.password <> pwd:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '文件夹不存在或密码错误'})
      try:
        f = UploadFile.objects.get(id=args['file_id'])
      except:
        return render_to_response('fileupload/uploadfail.html',
                                  {'error_message': '文件不存在'})
      os.remove(f.save_path.encode('utf-8'))
      f.delete()
      form = ListDirForm(initial={'dir': d})
      return render(request, 'fileupload/delete_success.html', 
                                {'form': form})
  else:
    form = DeleteConfirmForm()
#    form.password.label = '请输入{0}的密码'.format(args['dir'])
    return render(request, 'fileupload/delete_check.html', {
      'form': form, 
      'action': args['file_id'],
    })
