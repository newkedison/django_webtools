import os, sys

root = os.path.dirname(__file__)
sys.path.append(root)

print >> sys.stderr, "root_dir:", root
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
print >> sys.stderr, os.environ['DJANGO_SETTINGS_MODULE']
import django.core.handlers.wsgi
print >> sys.stderr, 'import ok'
application = django.core.handlers.wsgi.WSGIHandler()

# vim:ft=python
