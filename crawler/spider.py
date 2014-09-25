import os
import time
import calendar
import requests
from urlparse import urlparse
import MySQLdb as mdb
from crawler import CHROME_USER_AGENT


SPIDER_DATA = '/tmp'


def crawl_page(url, user_agent=CHROME_USER_AGENT):
    headers = { 'User-Agent': user_agent }
    resp = requests.get(url, headers=headers)
    return resp.text


def store_page(url, page_source, user_agent=CHROME_USER_AGENT):
    domain = urlparse(url).netloc

    # write meta_info
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor()
        prepared_statement = "insert into crawler VALUES(DEFAULT, %s, %s, %s, %s)"
        timestamp = calendar.timegm(time.gmtime())
        cur.execute(prepared_statement, (domain, url, user_agent, timestamp))
        page_id = cur.lastrowid

    # write source to file
    directory = '%s/%s/' % (SPIDER_DATA, domain)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = '%s/%s/%s' % (SPIDER_DATA, domain, page_id)
    with open(filename, 'w') as f:
        f.write(page_source.encode('utf-8'))


def crawl_and_store_page(url, user_agent=CHROME_USER_AGENT):
    page_source = crawl_page(url, user_agent)
    store_page(url, page_source, user_agent)


if __name__ == '__main__':
    crawl_and_store_page('http://stackoverflow.com/questions/2548493/in-python-after-i-insert-into-mysqldb-how-do-i-get-the-id')