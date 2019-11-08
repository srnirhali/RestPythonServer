# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 18:40:34 2019

@author: Dell
"""

import requests
from bs4 import BeautifulSoup

whitelist = [
  'p'
]     

def getAllPAndTitleTagsFormPage(url,title=False):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url,headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        ptags = soup.find_all('p')
        if(title):
            titletag = soup.find_all('title')
            return ptags,titletag
        else:
            return ptags
    else:
        return None


    