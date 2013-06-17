# Licence AGPL.



from bs4 import BeautifulSoup
import urllib, urllib2
import re
import json

#import html5lib Might want to use this instead of the default python parser.



api_url = "https://demo.openbankproject.com/obp/v1.1/banks/postbank/accounts/tesobe/public/transactions"

"""
Get company names out of OBP transaction data

"""
def get_company_names(api_url):
    company_names = []
    response = urllib2.urlopen(api_url)
    data = json.load(response)

    for transaction in data['transactions']:

        #print transaction['transaction']['other_account']['holder']['name']

        entity = transaction['transaction']['other_account']['holder']['name']
        is_alias = transaction['transaction']['other_account']['holder']['is_alias']

        if not is_alias:
            print 'Real name: %s ' % entity

            entity = entity.strip()
            if len(entity) > 2:
                company_names.append(entity)
            else:
                print 'Too short'
        else:
            print 'Alias: %s' % entity

    return frozenset(company_names) # Remove duplicates




"""
Use a search engine to find web pages which might contain the companies corporate address

"""
def get_possible_pages(company):
    link_set = []

    search_url = u'http://www.bing.com/search?q='
    search_url = '%s %s impressum' % (search_url, company)


    search_url = search_url.replace(' ', '+')
    search_url = search_url.encode("UTF-8")
    print 'search_url is %s' % search_url


    page = urllib2.urlopen(search_url)
    soup = BeautifulSoup(page.read())
    results = soup.find(id="results")
    for result in results.find_all("h3"):
        for link in result.find_all("a"):
            link_set.append(link.get('href'))
    return link_set[0:1]


def open_and_parse(company_name, url, recursion_level=0, addresses = []):

    company_name = company_name.lower()

    print 'Hello from open_and_parse. company_name is: %s url is %s recursion_level is %s addresses are %s' % (company_name, url, recursion_level, addresses)
    #import pdb; pdb.set_trace()


    try:
        page = urllib2.urlopen(url)
    except urllib2.URLError:
        print 'Trouble opening web page'


    #document = html5lib.parse(page.read)

    try:
        soup = BeautifulSoup(page.read())
    except:
        print 'Trouble parsing try: lxml or html5lib'




#######

    if recursion_level == 0:
        print 'Try to find Impressum link and go there..'
        for link in soup.find_all("a"):
            #import pdb; pdb.set_trace()
            if link.contents:
                #print link.contents
                if link.contents[0].find('impressum')> 0 or link.contents[0].find('Impressum')> 0:
                    print 'Found an impressum link. href to follow is %s' % link['href']

                    #import pdb; pdb.set_trace()
                    if recursion_level < 5:
                        recursion_level += 1

                        # If the href does not contain the domain, need to add it
                        next_url = link['href']
                        if not( next_url.find('http://') == 0 or next_url.find('https://') == 0):
                            next_url = '%s%s' % (url, next_url)

                        return open_and_parse(company_name, next_url, recursion_level, addresses)
    else:
        print 'Recursion level is not 0'
##########




    # print '====================================>'
    # print soup.prettify()
    # print '<===================================='

    #print(soup.get_text())


    #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    # Get rid script tags
    [s.extract() for s in soup('script')]


    # Remove html tags but don't squash and remove spaces
    # Only interested in text in the body

    text = soup.body.get_text(' , ').lower()




    #print "===================================="

    #print text

    #print "===================================="

    #print re.search('\d\d\d\d\d ', text).span()

    # Look for 5 digits and a space
    zip_search_result = re.search('\d\d\d\d\d ', text)

    if zip_search_result:
        zip_start, zip_end = zip_search_result.span()

        print 'zip_start is %s' % zip_start

        print 'zip text is %s' % text[zip_start:zip_start + 100]

        # Find the name of the company before this.

        # Find the last mention of the company before the zip
        company_start = text.rfind(company_name.strip(), 0, zip_start)
        print '%s company_start is %s' % (company_name, company_start)




        if zip_start - company_start > 1000:
            print 'Warning: grabbed too much text'
            # Try a shorter company name fragment.
            shorter_company_name = ''
            for co in company_name.strip().split(' '):
                print co
                shorter_company_name = ('%s %s ' % (shorter_company_name, co)).strip()

                print 'shorter_company_name is %s' % shorter_company_name
                company_start = text.rfind(shorter_company_name, 0, zip_start)

                if zip_start - company_start < 200:
                    break


                # if len(co) > 4:
                #     print 'adding %s' % co
                #     shorter_company_name = ('%s %s ' % (shorter_company_name, co)).strip()
                #
                #     print 'shorter_company_name is %s' % shorter_company_name
                # else:
                #     print 'ignoring'
            #company_start = text.rfind(shorter_company_name, 0, zip_start)
            print 'Now, %s company_start is %s' % (shorter_company_name, company_start)

            company_name = shorter_company_name

        print '%s company_start is %s' % (company_name, company_start)


        if company_start < 0:
            company_start = 0

        # how to find end of city?


        line_break_after_zip = text.find('\n', zip_end)

        something_after_zip = text.find('germany', zip_end)

        if something_after_zip == -1:
            something_after_zip = text.find('deutschland', zip_end)

        if something_after_zip == -1:
            something_after_zip = text.find('Telefon:', zip_end)

        if something_after_zip == -1:
            something_after_zip = text.find('telefon:', zip_end)


        if something_after_zip > -1 and something_after_zip < line_break_after_zip:
            address_end = something_after_zip
        else:
            address_end = line_break_after_zip

        # sanity check
        if address_end - zip_end > 50:
            address_end = zip_end + 50


        address_chunk = text[company_start: address_end]

        # hack to split the company name (which we already know) away from the address
        address_chunk = address_chunk.replace(company_name, company_name + " ")

        #print 'address chunk for company %s is \n %s' % (company_name, address_chunk)

        if len(address_chunk) > 200:
            print 'Warning: chunk is a bit long'

        addresses.append(address_chunk)

        print 'valid addresses for %s are %s' % (company_name, addresses)
        return addresses


    else:
        print 'Could not find zip code in page'
        for link in soup.find_all("a"):
            #print 'link is %s' % link
            # if link.title:
            #     if link.title.find('impressum')> 0 or link.title.find('Impressum')> 0:
            #         print '**** yeah we found an impressum link!'

            #import pdb; pdb.set_trace()
            if link.contents:
                #print link.contents
                if link.contents[0].find('impressum')> 0 or link.contents[0].find('Impressum')> 0:
                    print 'Found an impressum link. href to follow is %s' % link['href']

                    #import pdb; pdb.set_trace()
                    if recursion_level < 5:
                        recursion_level += 1

                        # If the href does not contain the domain, need to add it
                        next_url = link['href']
                        if not( next_url.find('http://') == 0 or next_url.find('https://') == 0):
                            next_url = '%s%s' % (url, next_url)

                        return open_and_parse(company_name, next_url, recursion_level, addresses)
                    else:
                        print 'Too deep'
                        return addresses






def find_corporate_address(company):
    print 'company is: %s' % company
    urls = get_possible_pages(company)

    company_name = company.lower()

    for url in urls:
        print 'Open %s for %s' % (url, company_name)
        print '*** Answer is: %s' % open_and_parse(company_name, url, 0, [])




if __name__=="__main__":

    #companies = ['Wooga GmbH', 'Host Europe GmbH', 'Music Pictures Ltd', 'cloudControl GmbH']
    #companies = ['Host Europe GmbH', 'Music Pictures Ltd', 'cloudControl GmbH']


    companies = ['FAIRNOPOLY EG I.GR']


    # Get companies mentioned in OBP transactions
    companies = get_company_names(api_url)


    for company in companies:
        find_corporate_address(company)