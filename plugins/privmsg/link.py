def main(data):
    args = argv('@',data['recv'])
    # look for URL
    link = geturl(data['recv'])
    if link and link != "" and not modeCheck('b', data):
        link = link[0]
        # look for title
        badext = ('.cgi','.CGI','.jpg','.png','.gif','.bmp')
        if not link[-4:] in badext:
            title = gettitle(link)
            if title:
                title = title.replace('\n',' ')
                title = title.replace('\r',' ')
                title = title.strip()
                if len(title) >= 150:
                    title = title[:150]
                title = title.encode('utf-8')
                title = html_decode(title)
                if len(link) > int(data['config']['settings']['maxLinkLen']):
                    # post title + tiny
                    data['api'].say(args['channel'], '^ ' + title + ' ' + maketiny(link) + ' ^')
                    return
                else:
                    # post title only
                    data['api'].say(args['channel'], '^ ' + title + ' ^')
                    return
        if len(link) > int(data['config']['settings']['maxLinkLen']):
            # post tiny only
            data['api'].say(args['channel'], '^ ' + maketiny(link) + ' ^')
            return
        else:
            # nothing
            return False
