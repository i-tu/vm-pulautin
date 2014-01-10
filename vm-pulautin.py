#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# viikkotiedote.py - Generoi Google-kalenterin ja Uutissyötteen perusteella viikkomailin.
#
# Koodannut Ian Tuomi, AS:n Tiedottaja 2011
#
# Omistettu Antti 'ATJ' Jaakkolalle <3
#

##############
## Settings ##
##############

gcal_username = 'tiedottaja@aski.hut.fi'
rss_url = 'http://sik.ayy.fi/fi/feeds/rss/news'

##################
## End settings ##
##################

from dateutil.parser import *
from datetime import date
from datetime import datetime
from datetime import timedelta
import gdata.calendar.service
import gdata.calendar  

import feedparser

paivat = {0:'ma', 1:'ti',2:'ke',3:'to',4:'pe',5:'la',6:'su'}

############################################################
# Haetaan syöte Google-kalenterista
############################################################

asCal = gdata.calendar.service.CalendarService()

start_date = date.today()
# Find the first and last days of next week
while start_date.weekday() != 0 : # Monday == 0 
    start_date += timedelta(1)
end_date = start_date + timedelta(7)

query = gdata.calendar.service.CalendarEventQuery(gcal_username, 'public', 'full')

query.start_min = str(start_date)
query.start_max = str(end_date) 
query.sortorder = 'ascending'
query.orderby = 'starttime'

feed = asCal.CalendarQuery(query)

start_date -= timedelta(7)
end_date -= timedelta(7)

# Fetch news
news_feed = feedparser.parse(rss_url)
# Sort in time order
news_feed.entries.sort(key=lambda entry: entry.updated_parsed.tm_yday)

############################################################
# Tulostetaan viikkomaili
############################################################

print u''
print u'Sisältö:'
print u''
print u'* Uutisia'
dex=0
for entry in news_feed.entries:
    if start_date <= date(entry.updated_parsed.tm_year, entry.updated_parsed.tm_mon, entry.updated_parsed.tm_mday) < end_date:
        print u'    1.%s %s %s.%s.' % (dex+1, entry.title, entry.updated_parsed.tm_mday, entry.updated_parsed.tm_mon)
        dex +=1
print u'* Tapahtumia'
for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
    d = parse(an_event.when[0].start_time)
    print u'    2.%s %s %s %s @ %s' % (i+1, an_event.title.text, paivat[d.weekday()], datetime.strftime(d,'%d.%m. %H.%M'), an_event.where[0].value_string)
print u"* Muuta"
print u''
print u'==========================================================='
print u'Uutiset'
print u'==========================================================='
print u''
dex = 0
for entry in news_feed.entries:
    if start_date < date(entry.updated_parsed.tm_year, entry.updated_parsed.tm_mon, entry.updated_parsed.tm_mday) < end_date:
        print u'1.%s %s %s.%s.' % (dex+1, entry.title, entry.updated_parsed.tm_mday, entry.updated_parsed.tm_mon)
        print u'-----------------------------------------------------------'
        print entry.summary
        print u''
        print u''
        dex += 1
print u'==========================================================='
print u'Tapahtumia'
print u'==========================================================='
for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
    print u''
    d = parse(an_event.when[0].start_time)
    print u'2.%s %s %s %s @ %s' % (i+1, an_event.title.text, paivat[d.weekday()], datetime.strftime(d,'%d.%m. %H.%M'), an_event.where[0].value_string)
    print u'-----------------------------------------------------------'
    print an_event.content.text
    print u''
print u''
print u'==========================================================='
print u'Muuta'
print u'==========================================================='
print u''