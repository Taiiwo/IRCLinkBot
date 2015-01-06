import re
import requests
from bs4 import BeautifulSoup
def get_content(url):
    paste = {
        'site': 'prntscr',
        'url':  url,
    }
    response = requests.get(url)
    if response.status_code !=200:
        return
    data = response.text
    soup = BeautifulSoup(data)
    url =  soup.find('meta', {'property': 'og:image'})['content']
    m = re.match('^.*/([a-zA-Z0-9]+)\.([a-zA-Z]+)$', url)
    response = requests.get(url)
    if response.status_code != 200 or not m:
        return

    paste['content'] = response.content
    paste['orig_filename'] = m.group(1)
    paste['ext'] = m.group(2)
    return paste

"""
url = 'http://prntscr.com/5ow1aq'
print get_content(url)
"""
