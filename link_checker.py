#-*- coding: utf-8 -*-
import sys, os, string
import socket, urllib, urllib2, httplib
import thread
from signal import SIGTERM
import simplejson
import socket, re

os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from settings import *
from directory.models import *


CLUBS = Club.objects.all()
# CLUBS = Club.objects.filter(id__in=[817, 591, 788, 946, 836])
for club in CLUBS:
    if club.homepage:
        try:
            urllib2.urlopen(club.homepage)
        except Exception, error:
            club.homepage = null
            club.save()
            print "%s (%s) has error %s" % (club.id, club.homepage, error)
