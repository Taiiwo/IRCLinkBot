def main(data):
    if "!wyr" in data['recv']:
        args = argv('!wyr',data['recv'])
        while 1:
            try:
            	retme = 'PRIVMSG '+ args['channel'] +' :' + gettitle('http://www.rrrather.com/view/' + str(random.randint(0,40000)))+ '\r\n'
                return retme
            except:
                print '[Server Error (Not my fault)]'
