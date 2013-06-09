from bs4 import BeautifulSoup
import urllib2
import re
import json

api_url = "https://demo.openbankproject.com/obp/v1.1/banks/postbank/accounts/tesobe/public/transactions"


def get_company_names(api_url):
    page = urllib2.urlopen(api_url)
    json_contents = response.read()

def build_searchurl(company):
    searchurl = "http://www.bing.com/search?q="
    comp = company.split(' ')
    for word in comp:
        searchurl = searchurl + '+' + word
    searchurl = searchurl + '+' + 'impressum'
    return searchurl


def get_link_set(company):
    searchurl = build_searchurl(company)
    link_set = []
    page = urllib2.urlopen(searchurl)
    soup = BeautifulSoup(page.read())
    results = soup.find(id="results")
    for result in results.find_all("h3"):
        for link in result.find_all("a"):
            link_set.append(link.get('href'))
    return link_set


companies = ['Wooga GmbH', 'Host Europe GmbH', 'Music Pictures Ltd']
for comp in companies:
    link_set = get_link_set(comp)

# go to google searching for company_name + "impressum"

# Find first URL
#company_name = "HOST EUROPE GMBH".lower()
#url="http://www.hosteurope.de/Impressum/"

#company_name = "Wooga GmbH".lower()
#url = "http://www.wooga.com/legal/contact/"

#company_name = "Music Pictures Ltd".lower()
#url = "http://www.tesobe.com/en/contact-imprint/"


#company_name = "cloudControl GmbH".lower()
#url = "https://www.cloudcontrol.com/imprint"

company_name = "Txtr".lower()
url = "http://de.txtr.com/imprint/"



company_name = "weihenstephan"
url = "http://weihenstephaner.de/fallback/impressum.html"



page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
# print '====================================>'
# print soup.prettify()
# print '<===================================='

#print(soup.get_text())


print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


text = soup.get_text(' , ').lower()


print "===================================="

print text

print "===================================="

print re.search('\d\d\d\d\d ', text).span()

# Look for 5 digits and a space
zip_start, zip_end = re.search('\d\d\d\d\d ', text).span()

print 'zip_start is %s' % zip_start

# Find the name of the company before this.

# Find the last mention of the company before the zip
company_start = text.rfind(company_name.strip(), 0, zip_start)



print '%s company_start is %s' % (company_name, company_start)


if company_start < 0:
     company_start = 0

# how to find end of city?


line_break_after_zip = text.find('\n', zip_end)

germany_after_zip = text.find('germany', zip_end)

if germany_after_zip == -1:
    germany_after_zip = text.find('deutschland', zip_end)

if germany_after_zip > -1 and germany_after_zip < line_break_after_zip:
    address_end = germany_after_zip
else:
    address_end = line_break_after_zip

# sanity check
if address_end - zip_end > 50:
    address_end = zip_end + 50


address_chunk = text[company_start: address_end]

# hack to split the company name (which we already know) away from the address
address_chunk = address_chunk.replace(company_name, company_name + " ")

print 'address chunk is \n %s' % address_chunk
