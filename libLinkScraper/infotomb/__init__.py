#!/usr/bin/env python
import requests
import re
from bs4 import BeautifulSoup
def get_content(url):
    paste_info = {
        'site': 'infotomb',
        'url': url,
    }
    response = requests.get(url)
    if response.status_code != 200:
        return
    m = re.match('^.*/([0-9a-zA-Z]+)((\.[a-zA-Z]+)*)$',url)
    if not m.group(2):
        data = response.text
        soup = BeautifulSoup(data)
        url = soup.find_all('input')[2]['value']
        m = re.match('^.*/([0-9a-zA-Z]+)((\.[a-zA-Z]+)*)$',url)
        if m:
            response = requests.get(url)
            if response.status_code != 200:
                return
        else:
           return

    idd = m.group(3)[1:]
    paste_info['content'] = response.content
    paste_info['orig_filename'] = m.group(1)
    paste_info['ext'] = idd
    return paste_info

'''
url = 'https://infotomb.com/y53jc'
print get_content(url)
'''
