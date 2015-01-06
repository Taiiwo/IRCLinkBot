#!/usr/bin/env python
import requests
import re
def get_content(url):
    paste_info = {
        'site': 'cubeupload',
    }
    m = re.match('^.*om(?:/(im))?/([0-9a-zA-Z]+)\.([a-zA-Z]+)$',url) # note that cubeupload enforces file extensions
    if m.group(1) == 'im':
        url = 'http://i.cubeupload.com/' + m.group(2) + '.' + m.group(3)
        paste_info['extension'] = m.group(3)
        paste_info['orig_filename'] = m.group(2)
    response = requests.get(url)
    if response.status_code != 200:
        return
    paste_info['url'] = url
    paste_info['extension'] = m.group(3)
    paste_info['orig_filename'] = m.group(2)
    paste_info['content'] = response.content
    return paste_info
'''
url = 'http://cubeupload.com/im/P7XnyV.jpg'
print get_content(url)
'''
