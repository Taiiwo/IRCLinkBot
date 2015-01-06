#!/usr/bin/env python

import re
import requests


def get_content(url):
    base_url = "https://cache.gyazo.com/%s.png"
    paste_info = {
        'site': 'gyazo',
        'url': url,
    }
    m = re.search("[a-z0-9]{32}", url)
    if m is None:
        return

    img_id = m.group(0)
    content_url = base_url % img_id
    
    response = requests.get(content_url)
    if response.status_code != 200:
        return

    paste_info['ext'] = ""
    paste_info['orig_filename'] = img_id
    paste_info['content'] = response.content
    return paste_info

