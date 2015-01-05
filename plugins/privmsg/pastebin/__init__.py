#!/usr/bin/env python

import requests


def get_content(url):
    paste_info = {
        'site': 'pastebin',
        'url': url,
    }
    if "raw.php" in url:  # http://pastebin.com/raw.php?i=gpRREVYd
        # dissolve the key=value pairs
        param_str_raw = url[url.index('?')+1:]
        params = {k: v for (k, v) in (
            kv.split('=') for kv in param_str_raw.split('&'))}

        paste_id = params.get('i')
        if paste_id is None:  # no i parameter
            return

        content_url = url

    else:
        base_str = "http://pastebin.com/raw.php?i="
        paste_id = url.split('/')[-1]

        content_url = base_str + paste_id

    response = requests.get(content_url)
    if response.status_code != 200:
        return

    paste_info['ext'] = ""
    paste_info['orig_filename'] = paste_id
    paste_info['content'] = response.content
    return paste_info

