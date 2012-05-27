from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

def index(request):
  return render_to_response('index.html')

def robots(request):
  import os
  s = open(os.path.join(os.path.dirname(__file__), "templates/robots.txt"), "rb").read()
  response = HttpResponse(s, mimetype='text/plain')
#if add the below line, then the browser will open a download window instead of showing the content of file
#  response['Content-Disposition'] = 'attachment; filename=robots.txt'
  return response
