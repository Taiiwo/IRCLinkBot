#!/usr/bin/env python

import requests


def get_content(url):
    paste_info = {
        'site': 'hastebin',
        'url': url,
    }
    site_suffix = ".hs"  # hastebin suffixes pastes with ".hs" unless raw mode
    base_url = "http://hastebin.com/raw/%s"

    if url.endswith(".hs"):  # we dont have a raw url
        orig_filename = url.split('/')[-1]
        paste_id = orig_filename.split('.')[0]
        content_url = base_url % paste_id
    else:  # we do have a raw url
        paste_id = url.split('/')[-1]
        orig_filename = paste_id + site_suffix
        content_url = url

    response = requests.get(content_url)

    if response.status_code != 200:
        return

    paste_info['ext'] = ""
    paste_info['orig_filename'] = orig_filename
    paste_info['content'] = response.content
    return paste_info
