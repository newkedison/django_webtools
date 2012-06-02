# Create your views here.
#encoding: utf-8
import os
import re
import sys #for print >> sys.stderr, 'some log'
import tempfile
import datetime
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from models import Directory, UploadFile
from forms import UploadForm, ListDirForm, DeleteConfirmForm

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
  if f.auto_delete_days > 0 and \
     f.upload_date + datetime.timedelta(days=f.auto_delete_days) \
     < datetime.datetime.now():
    check_used(d)
    raise Http404
  wrapper = FileWrapper(file(f.save_path.encode('utf-8')))
  response = HttpResponse(wrapper, content_type=f.content_type)
  response['Content-Length'] = os.path.getsize(f.save_path.encode('utf-8'))
  x = response['Content-Length']
  if args['method'] == 'get':
    response['Content-Disposition'] = 'attachment; filename={0}'.format(f.file_name)
  f.download_count += 1
  f.save()
  return response

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

def discuss(request):
  return render_to_response('fileupload/discuss.html')
