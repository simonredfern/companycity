# Licence AGPL.



from bs4 import BeautifulSoup
import urllib, urllib2
import re
import json

import elasticsearch


#import html5lib Might want to use this instead of the default python parser.



api_url = "https://api.openbankproject.com/obp/v1.2.1/banks/postbank/accounts/tesobe/public/transactions"

# See http://www.elasticsearch.org/blog/unleash-the-clients-ruby-python-php-perl/#python


# obp_limit


"""
Get transactions and push them to Elastic Search.

"""
def push_transactions_to_elastic_search(api_url):
    company_names = []
    response = urllib2.urlopen(api_url)
    data = json.load(response)


    es = elasticsearch.Elasticsearch()



    i = 0

    for transaction in data['transactions']:
        i = i + 1

        print 'transaction: %s' % transaction


        id = transaction['id']


        #print 'this %s' % transaction['this_account']
        #
        #other_holder_name = transaction['other_account']['holder']['name']
        #
        #print 'other %s' % other_holder_name
        #
        ##                 "date": date(2013, 9, 24),



        print 'insert %s' % id
        # Index a document:
        insert_doc = es.index(
            index="obp_001",
            doc_type="transaction",
            id=id,
            body=transaction
        )

        print 'insert_doc  is %s' % insert_doc


        # Get the document:
        get_doc = es.get(index="obp_001", doc_type="transaction", id=id)



        print 'get_doc id %s is %s' % (id, get_doc)



    return 'ok'





if __name__=="__main__":
    result = push_transactions_to_elastic_search(api_url)


