def main(data):
        args = argv('@',data['recv'])
        urlsfound = True
        try:#look for urls in recv
                link = geturl(data['recv'])
                if link == '':
                        raise Exception("No links found.")
                error = 0
        except Exception , err:
                print sys.exc_info()[1]
                print "[-]No URLS found"
                error = 1
                urlsfound = False
        try:#try to get the title of the url
                nlink = link[0]
                badext = ('.cgi','.CGI','.jpg','.png','.gif','.bmp')
                if nlink[-4:] in badext:# don't process images and stuff
                        pass
                else:#only get one line of titles
                        title = gettitle(nlink)
                        title = title.splitlines()
                        title = ''.join(title)
                if len(title) >= 150:#cap the length of titles
                        title = title[:150]
                title = html_decode(title)
                title = title.encode('ascii', 'ignore')
                print title
                error = 0
        except:
                print "[E]No valid title"
                if not 'http' in data['recv']:
                        urlsfound = False
                error = 2
        #post title to irc
        if error == 0 and data['loop'] >= int(data['config']['variables']['numr']):
                slink = nlink.decode("utf-8")
                nlink = slink.encode("ascii","ignore")
                if len(nlink) >= 53:
                        return 'privmsg ' + args['channel'] + ' :^ ' + str(title) + " " + maketiny(nlink) + ' ^\r\n'
                else:
                        return 'privmsg ' + args['channel'] + ' :^ ' + str(title) + " ^\r\n"
        if error == 2 and urlsfound and nlink != "" and data['loop'] >= data['numr'] and len(nlink) >= 53:
                return 'privmsg ' + args['channel'] + ' : ^ ' + maketiny(nlink) + ' ^\r\n'
        else:
                return ''


