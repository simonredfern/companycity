from bs4 import BeautifulSoup
import urllib2
import re
import json


api_url = "https://demo.openbankproject.com/obp/v1.1/banks/postbank/accounts/tesobe/public/transactions"


def get_company_names(api_url):
    company_names = []
    response = urllib2.urlopen(api_url)
    data = json.load(response)

    for transaction in data['transactions']:

        #print transaction['transaction']['other_account']['holder']['name']

        entity = transaction['transaction']['other_account']['holder']['name']
        is_alias = transaction['transaction']['other_account']['holder']['is_alias']

        if not is_alias:
            print 'Not an alias, - Use %s ' % entity

            entity = entity.strip()
            if len(entity) > 2:
                company_names.append(entity)
            else:
                print 'Too short'
        else:
            print 'Is an alias, - Skip %s' % entity

    return frozenset(company_names) # Remove duplicates






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
    return link_set[0:1]


#companies = ['Wooga GmbH', 'Host Europe GmbH', 'Music Pictures Ltd', 'cloudControl GmbH']
#companies = ['Host Europe GmbH', 'Music Pictures Ltd', 'cloudControl GmbH']

companies = get_company_names(api_url)


for company in companies:
    link_set = get_link_set(company)

    valid_company_addresses = []


    # go to google searching for company_name + "impressum"

    company_name = company.lower()

    for url in link_set:

        # Find first URL
        #company_name = "HOST EUROPE GMBH".lower()
        #url="http://www.hosteurope.de/Impressum/"

        #company_name = "Wooga GmbH".lower()
        #url = "http://www.wooga.com/legal/contact/"

        #company_name = "Music Pictures Ltd".lower()
        #url = "http://www.tesobe.com/en/contact-imprint/"


        #company_name = "cloudControl GmbH".lower()
        #url = "https://www.cloudcontrol.com/imprint"

        # company_name = "Txtr".lower()
        # url = "http://de.txtr.com/imprint/"
        #
        # company_name = "weihenstephan"
        # url = "http://weihenstephaner.de/fallback/impressum.html"


        print 'about to open %s for %s' % (url, company_name)


        try:
            page = urllib2.urlopen(url)
        except urllib2.URLError:
            print 'Trouble opening web page'
            continue

        try:
            soup = BeautifulSoup(page.read())
        except:
            print 'Trouble parsing try: lxml or html5lib'
            continue



        # print '====================================>'
        # print soup.prettify()
        # print '<===================================='

        #print(soup.get_text())


        #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        # Remove html tags but don't squash and remove spaces
        text = soup.get_text(' , ').lower()


        #print "===================================="

        #print text

        #print "===================================="

        #print re.search('\d\d\d\d\d ', text).span()

        # Look for 5 digits and a space

        zip_search_result = re.search('\d\d\d\d\d ', text)

        if zip_search_result:


            zip_start, zip_end = zip_search_result.span()

            #print 'zip_start is %s' % zip_start

            # Find the name of the company before this.

            # Find the last mention of the company before the zip
            company_start = text.rfind(company_name.strip(), 0, zip_start)



            #print '%s company_start is %s' % (company_name, company_start)


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

            #print 'address chunk for company %s is \n %s' % (company_name, address_chunk)

            if len(address_chunk) < 100:
                valid_company_addresses.append(address_chunk)

        else:
            print 'Could not find zip code in page'

    print 'valid addresses for %s are %s' % (company_name, valid_company_addresses)