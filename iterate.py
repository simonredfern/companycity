from bs4 import BeautifulSoup
import urllib2
import re

companies = ['Wooga GmbH', 'Host Europe GmbH', 'Music Pictures Ltd']
complist = []
for comp in companies:
    searchurl = "http://www.bing.com/search?q="
    comp = comp.split(' ')
    for word in comp:
        searchurl = searchurl + '+' + word
    searchurl = searchurl + '+' + 'imprint'
    print searchurl
    page = urllib2.urlopen(searchurl)
    soup = BeautifulSoup(page.read())
    # print soup.prettify()
    results = soup.find(id="results")
    for result in results.find_all("h3"):
        for link in result.find_all("a"):
            print(link.get('href'))
    # print resultsblock.find("h3",{"class":"r"})
