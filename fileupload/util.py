#encoding: utf-8
import os
import sys #for print >> sys.stderr, 'some log'
import tempfile
import datetime
from models import UploadFile
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

