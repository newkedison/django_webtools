# Create your views here.
#encoding: utf-8
import os
import tempfile
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from models import Directory, UploadFile

class UploadForm(forms.Form):
  directory = forms.CharField(label='文件夹', max_length=100, 
    help_text='文件要保存在哪一个文件夹内.注意,这个文件夹必须已存在.')
  password = forms.CharField(label='密码', max_length=100,
    help_text='该文件夹的上传密码')
  filename = forms.CharField(label='文件名', max_length=30,
    help_text='文件被下载时使用的文件名,不能和同文件夹内的其他已存在的文件重复')
  auto_delete = forms.CharField(label='自动删除时间(单位:天)', initial=0,
    help_text='达到指定天数后,该文件会自动删除,设为0表示不自动删除')
  description = forms.CharField(label='文件描述', required=False,
    help_text='对文件的描述,可以为空', widget=forms.Textarea)
  file = forms.FileField(label='待上传文件')
 
def get_save_path(file_name):
  _, filename = os.path.split(file_name)
  prefix, suffix = os.path.splitext(filename)
  path = os.path.join(os.path.dirname(__file__), 'files')
  if not os.path.exists(path):
    os.makedirs(path)
  _, filename = tempfile.mkstemp(suffix, prefix+"_", path)
  return filename

def handle_upload_file(query, f, form_data):
  min_block = 4 * 1024
  size = f.size
  space = (f.size + min_block - 1) / min_block * min_block
  if form_data['filename'] <> '':
    name = form_data['filename']
  else:
    name = f.name
  save_path = get_save_path(name)
  UploadFile.objects.create(directory=query, 
                            file_name=name,
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

def index(request, *arg, **args):
  return render_to_response('fileupload/index.html')

def upload(request):
  if request.method == 'POST':
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
      form_data = form.cleaned_data
      d = Directory.objects.filter(directory=form_data['directory'])
      if d and d[0].password == form_data['password']:
        handle_upload_file(d[0], request.FILES['file'], form_data)
        return HttpResponseRedirect('success')
      else:
        return HttpResponse('failed')
    else:
      return render(request, 'fileupload/upload.html', {'form': form})
  else:
    form = UploadForm()
    return render(request, 'fileupload/upload.html', {'form': form})

def success(request):
  return HttpResponse('<a href="index">go to index</a><br><a href="upload">upload another file</a>')
