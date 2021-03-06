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
from forms import UploadForm, DirPasswordForm, DeleteConfirmForm
from util import get_save_path, handle_upload_file, check_used

def index(request, *arg, **args):
  return render_to_response('fileupload/index.html',
        {'login_dir': request.session.get('dir', ''), })

def upload(request):
  if request.method == 'POST':
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
      form_data = form.cleaned_data
      try:
        d = Directory.objects.get(directory=form_data['directory'])
      except:
        return HttpResponseRedirect('../failed/?e=' + '文件夹不存在或密码错误')
      if not d.check_password(form_data['password']):
        return HttpResponseRedirect('../failed/?e=' + '文件夹不存在或密码错误')
      f = request.FILES['file']
      name = form_data['filename'] if form_data['filename'] <> '' else f.name
      if UploadFile.objects.filter(directory=d, file_name=name).count() <> 0:
        return HttpResponseRedirect('../failed/?e=' + '该文件名已存在')
      if f.size > d.file_max_size * 1024 * 1024:
        return HttpResponseRedirect('../failed/?e=' \
                                    + '文件大小超过文件夹允许单个文件的上限')
      check_used(d)
      if f.size + d.used_size > d.total_size * 1024 * 1024:
        return HttpResponseRedirect('../failed/?e=' + '文件夹已满')
      try:
        handle_upload_file(d, f, name, form_data)
      except:
        return HttpResponseRedirect('../failed/?e=' + '保存文件失败')

      return HttpResponseRedirect(
        '../success/?u={0:.3f}&t={1}&d={2}&fs={3}&on={4}&nn={5}'.format(
        d.used_size / 1024.0 / 1024, d.total_size, d, f.size, 
          f.name.encode('utf-8'), name.encode('utf-8')))
  else:
    form = UploadForm()
  return render(request, 'fileupload/upload.html', 
                {'form': form,
                 'login_dir': request.session.get('dir', ''),
                })

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
    'login_dir': request.session.get('dir', ''),
  })

def failed(request):
  error = request.GET.get('e', '')
  return render_to_response('fileupload/fail.html', {
    'error_message': error,
    'login_dir': request.session.get('dir',''),
  })

def list_dir(request, *arg, **args):
  s_dir = request.session.get('dir', '')
  a_dir = args.get('dir', '')
  if not a_dir:
    a_dir = ''
  if a_dir == '' and s_dir == '':
    return HttpResponseRedirect('/files/check')
  if a_dir <> '' and s_dir <> a_dir:
    return HttpResponseRedirect('/files/check')
  if a_dir == '':
    return HttpResponseRedirect('/files/list/{0}'.format(s_dir))

  d = get_object_or_404(Directory, directory=s_dir)
  if request.session.get('check', '') <> d.password:
    return HttpResponseRedirect('/files/check')

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
    'login_dir': request.session.get('dir', ''),
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
        return HttpResponseRedirect('../../../failed/?e=' \
                                    + '文件夹不存在或密码错误')
      if not d.check_password(pwd):
        return HttpResponseRedirect('../../../failed/?e=' \
                                    + '文件夹不存在或密码错误')
      try:
        f = UploadFile.objects.get(id=args['file_id'])
      except:
        return HttpResponseRedirect('../../../failed/?e=' + '文件不存在')
      os.remove(f.save_path.encode('utf-8'))
      f.delete()
      return render(request, 'fileupload/delete_success.html', 
                              {'url': '../../../list/{0}/'.format(d.directory), 
                               'login_dir': request.session.get('dir', ''),})
  else:
    form = DeleteConfirmForm()
  return render(request, 'fileupload/delete_check.html', {
    'form': form, 
    'action': '../' + args['file_id'] + '/',
    'login_dir': request.session.get('dir', ''),
  })

def discuss(request):
  return render_to_response('fileupload/discuss.html', {
    'login_dir': request.session.get('dir', ''),
  })

def check(request, *arg, **args):
  next = request.GET.get('next', '')
  if request.method == 'POST':
    form = DirPasswordForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      try:
        d = Directory.objects.get(directory=form_data['directory'])
      except:
        return HttpResponseRedirect('../failed/?e=' + '文件夹不存在或密码错误')
      if not d.check_password(form_data['password']):
#      if d.password <> form_data['password']:
        return HttpResponseRedirect('../failed/?e=' + '文件夹不存在或密码错误')
      request.session['dir'] = d.directory
      request.session['check'] = d.password
      request.session.set_expiry(0)
      if next == '':
        next = '../list/'
      return HttpResponseRedirect(next)
  else:
    form = DirPasswordForm()
  return render(request, 'fileupload/check.html', {
    'form': form, 
    'action': './?next={0}'.format(next) if next <> '' else '.',
    'login_dir': request.session.get('dir', ''),
  })



