#!/usr/bin/env python
"""Get articles from owler
Owler puts articles behind an iframe, so it requires a few steps to get. Also it involves running the javascript
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import re
import time
from crawler.ratelimiter import rate_limited


@rate_limited(0.2)
def get_owler_article_pages(driver, url):
    """Get owler article url on a owler news page for a company

    Parameters
    ----------
    driver : WebDriver
        webdriver, usually PhantomJS
    url : str
        owler news url
        example - https://www.owler.com/iaApp/100242/uber-news
    """
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    feed = soup.find('ul', {'class': 'feeds_list'})
    urls = []
    for item in feed.findAll('li'):
        url = item.find('a', {'class' : 'feedTitle'})['href']
        urls.append(url)
    return urls


@rate_limited(0.2)
def get_url_from_owler_article_page(driver, url):
    """Get url from an owler article page

    Parameters
    ----------
    driver : WebDriver
        webdriver, usually PhantomJS
    url : str
        owler article url
        example - http://www.owler.com/iaApp/article/541cf77ce4b0e71dc7cd7d14.htm
    """
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    script = soup.findAll('script')[-1]
    return re.search('location = "(?P<url>.+)"', str(script)).group('url')


def run():
    driver = webdriver.PhantomJS()

    url = 'https://www.owler.com/iaApp/100242/uber-news'
    urls = get_owler_article_pages(driver, url)
    print urls

    print get_url_from_owler_article_page(driver, urls[0])

    driver.close()
    driver.quit()


def main():
    run()


if __name__ == '__main__':
    main()
