#!/usr/bin/env python

import requests


def get_content(url):
    base_url = "http://p.pomf.se/?dl="
    paste_info = {
        'site': 'ppomf',
        'url': url,
    }

    paste_id = url.split('/')[-1]

    content_url = base_url + paste_id
    response = requests.get(content_url)

    if response.status_code != 200:
        return

    paste_info['ext'] = ""
    paste_info['orig_filename'] = paste_id
    paste_info['content'] = response.content

    return paste_info
