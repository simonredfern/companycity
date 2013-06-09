from bs4 import BeautifulSoup
import urllib2

import re

def found_zip(text):
# 51149

    pos = text.find('51149')

    if pos > -1:
        print 'pos is %s' % pos
        return True
    else:
        return False


companies = ['Wooga GmbH', 'Host Europe GmbH', 'Music Pictures Ltd']
complist = []
for comp in companies: 
    searchurl = "http://www.google.com/#q="
    comp = comp.split(' ')
    for word in comp:
        searchurl = searchurl+'+'+word
    searchurl = searchurl+'+'+'imprint'
    page=urllib2.urlopen(searchurl)
    soup = BeautifulSoup(page.read())
    resultsblock = soup.find("ol", {"id":"rso"})
    resultsblock.find("h3",{"class":"r"})

company_name = "HOST EUROPE GMBH".lower()

# go to google searching for company_name + "impressum"

# Find first URL

url="http://www.hosteurope.de/Impressum/"

company_name = "Wooga GmbH".lower()
url = "http://www.wooga.com/legal/contact/"




page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
# print '====================================>'
# print soup.prettify()
# print '<===================================='

#print(soup.get_text())

print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

if found_zip(soup.get_text()):
    print "yes"
else:
    print "no"



p = re.compile("\d")
s = p.search(soup.get_text())

print "search result is %s" % s

text = soup.get_text().lower()


# print text

print re.search('\d\d\d\d\d ', text).span()

# Look for 5 digits and a space
zip_start, zip_end = re.search('\d\d\d\d\d ', text).span()

print 'zip_start is %s' % zip_start

# Find the name of the company before this.

# Find the last mention of the company before the zip
company_start = text.rfind(company_name, 0, zip_start)

print 'company_start is %s' % company_start

if company_start < 0:
    company_start = 0

# how to find end of city?


line_break_after_zip = text.find('\n', zip_end)



address_chunk = text[company_start: line_break_after_zip]

print 'address chunk is \n %s' % address_chunk
