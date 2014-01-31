def main(data):
        if '!joke' in data['recv']:
                args = argv('!joke',data['recv'])
                while 1:
                        html = urllib2.urlopen('http://www.sickipedia.org/random').read()
                        soup = BeautifulSoup(html)
                        joke = soup.body.find('section', attrs={'class':'jokeText'}).text #div -> section. It works.
                        #   joke = unicode(joke) 1 problem I've found - jokes are not nearly as funny as they used to be
                        if len(joke) <= 250:
                                joke = joke.replace('\n', ' ')
                                joke = joke.decode("utf-8")
                                joke = html_decode(joke.encode("ascii","ignore"))
                                return 'privmsg ' + args['channel'] + ' :' + joke + '\r\n'
                return 'privmsg ' + args['channel'] + ' :' + joke + '\r\n'
