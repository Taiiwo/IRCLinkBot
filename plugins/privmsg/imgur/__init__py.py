#!/usr/bin/env python
import requests
import re
from bs4 import BeautifulSoup
def get_content(url):
    paste_info = {
        'site': 'imgur',
        'url': url
    }
    m = re.match('^.*com(?:/gallery)?/([0-9a-zA-Z]+)(?:\.([a-zA-Z]+))?$',url)
    response = requests.get(url)
    if response.status_code != 200:
        return
    if not m.group(2):
        soup = BeautifulSoup(response.text)
        url1 =  soup.find('meta', {'property': 'og:image'})['content']
        m = re.match('^.*com/([0-9a-zA-Z]+)\.([a-zA-Z]+)$',url1)
        response = requests.get(url1)
        if response.status_code != 200:
            return
    paste_info['extension'] = m.group(2)
    paste_info['orig_filename'] = m.group(1)
    paste_info['content'] = response.content
    return paste_info
'''
url = 'http://imgur.com/gallery/aChgMdG'
print get_content(url)
'''
