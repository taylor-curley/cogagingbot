#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import datetime
import feedparser
from bs4 import BeautifulSoup

# Get date and time for log
time = datetime.datetime.now()

################################################################################
# Elsevier journal websites #
ejournal_web = [
"http://www.journals.elsevier.com/experimental-gerontology/recent-articles", 
"http://www.journals.elsevier.com/mechanisms-of-ageing-and-development/recent-articles", 
"http://www.journals.elsevier.com/ageing-research-reviews/recent-articles"
]

# Elsevier journal titles (cannot exceed 50 characters)
ejournal_title = [
"Experimental Gerontology", 
"Mechanisms of Ageing and Development",
"Ageing Research Reviews"
]

etitle = []
eurl = []
ejournal = []

# Loop through core Elsevier journals
y = 0
for x in ejournal_web:
    # Read site
    o = urllib.request.urlopen(ejournal_web[y])
    site = BeautifulSoup(o, "lxml")
    
    # Pull 3 most current postings (rawish data)
    titleOne = site.find_all("div", class_="pod-listing-header", limit=3)
    titleOne = BeautifulSoup(str(titleOne), 'html.parser')
    titleTwo = titleOne.find_all("a", title=True)
    
    # Keep track of published articles
    f = open('/home/taylor/Documents/bots/cogaging/tweeted_pubs_cab.txt', 'a+')
    g = open('/home/taylor/Documents/bots/cogaging/tweeted_pubs_cab.txt', 'r')
    g = [line.rstrip('\n') for line in g]
    
    for i in range(3):
        entry = titleTwo[i]['title']
        if entry in g:
            print('Redundant entry... ' + str(time))
        else:
            etitle.append(titleTwo[i]['title'])
            eurl.append(titleTwo[i]['href'])
            ejournal.append(str(ejournal_title[y]))
            # Log article names + URLs 
            f.write(str(entry) + '\n' + str(titleTwo[i]['href']) + '\n')  
              
    f.close()
    y = y + 1


################################################################################
# Loop through core Springer,T&F, Cell, and APA journal websites

sjournal_web = [
"http://content.apa.org/journals/pag-ofp.rss", 
"http://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=nanc20", 
"http://psychsocgerontology.oxfordjournals.org/rss/ahead.xml"

]

sjournal_title = [
"Psychology and Aging", 
"Aging, Neuropsychology, and Cognition", 
"Journals of Gerontology: Series B"
]

stitle = []
surl = []
sjournal = []

y = 0
for x in sjournal_web:
    # Read XML feed
    site = feedparser.parse(sjournal_web[y])

    # Keep track of published articles
    f = open('/home/taylor/Documents/bots/cogaging/tweeted_pubs_cab.txt', 'a+')
    g = open('/home/taylor/Documents/bots/cogaging/tweeted_pubs_cab.txt', 'r')
    g = [line.rstrip('\n') for line in g]

    for i in range(len(site['entries'])):
        entry = site['entries'][i]['title']
        entry_url = site['entries'][i]['link']
        if entry in g:
            print('Redundant entry... ' + str(time))
        else:
            # Log article names + URLs 
            stitle.append(site['entries'][i]['title'])
            surl.append(site['entries'][i]['link'])
            sjournal.append(sjournal_title[y])
            f.write(str(entry) + '\n' + str(entry_url) + '\n') 
              
    f.close()
    y = y + 1


###############################################################################
# Search non-aging journals for content: Elsevier

fjournal_web = [
'http://www.journals.elsevier.com/cognitive-psychology/recent-articles', 
'http://www.journals.elsevier.com/acta-psychologica/recent-articles', 
'http://www.journals.elsevier.com/brain-and-cognition/recent-articles', 
'http://www.journals.elsevier.com/cognition/recent-articles', 
'http://www.journals.elsevier.com/consciousness-and-cognition/recent-articles', 
'http://www.journals.elsevier.com/journal-of-memory-and-language/recent-articles', 
'http://www.journals.elsevier.com/neuropsychologia/recent-articles', 
'http://www.journals.elsevier.com/trends-in-cognitive-sciences/recent-articles', 
'http://www.journals.elsevier.com/journal-of-applied-research-in-memory-and-cognition/recent-articles'
]

fjournal_title = [
"Cognitive Psychology", 
"Acta Psychologica",
"Brain and Cognition", 
"Cognition", 
"Consciousness and Cognition",
"Journal of Memory and Language", 
"Neuropsychologica", 
"Trends in Cognitive Sciences", 
"Applied Research in Memory & Cognition"
]

keywords = [
"aging", 
"Aging", 
"aged",
"Aged",
"adult development", 
"Adult development",
"older",
"Older",  
"age-related",
"Age-related",
"age-deficits",
"Age-deficits"
]

ftitle = []
furl = []
fjournal = []

y = 0

for t in range(len(fjournal_web)):
    
    found = []
    o = urllib.request.urlopen(fjournal_web[t])
    site = BeautifulSoup(o, "lxml")
    titleOne = site.find_all("div", class_="pod-listing-header")
    titleOne = BeautifulSoup(str(titleOne), 'html.parser')
    titleTwo = titleOne.find_all("a", title=True)
    
    for i in range(len(titleTwo)):
        if any(x in titleTwo[i]['title'] for x in keywords):
            found.append(i)
            
    f = open('/home/taylor/Documents/bots/cogaging/tweeted_pubs_cab.txt', 'a+')
    g = open('/home/taylor/Documents/bots/cogaging/tweeted_pubs_cab.txt', 'r')
    g = [line.rstrip('\n') for line in g]
        
    for p in range(len(found)):
        entry = titleTwo[found[p]]['title']
        if entry in g:
            print('Redundant entry... ' + str(time))
        else:
            ftitle.append(entry)
            furl.append(titleTwo[found[p]]['href'])
            fjournal.append(str(fjournal_title[t]))
            # Log article names + URLs 
            f.write(str(entry) + '\n' + str(titleTwo[p]['href']) + '\n')  
            print('Found "' + entry + '"')
                
    f.close()
    y = y + 1
