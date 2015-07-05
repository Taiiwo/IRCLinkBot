# Find IP plugin for Taiiwobot by zingmars
# All maintaining duties still go to Taiiwo
# This plugin was tested on the live session of Taiiwobot, and it crashed
# TaiiwoBot   1   times during dev. (wasn't my fault, I swear)
def main(data):
    if '!findip ' in data['recv']:
        args = argv('!findip', data['recv'])
        # GET whois data
        query = ' '.join(args['argv'][1:])
        import urllib
        query = urllib.quote(query)
        try:
            # This service can take up to 15k requests per hour. Try not to overuse it.
            whois = urllib2.urlopen('http://ip-api.com/json/' + query + '?fields=65535')
            answ = json.load(whois)
        except:
            data['api'].say( args['channel'], 'API Error.' )
            return

        # Mad error handling skills (from coinprice plugin)
        try:
            if answ == False: # Closest I could find to checking for null
                data['api'].say( args['channel'], 'General JSON failure.' )
                return
        except:
            pass
        if answ['status']  == 'success':
            # prepare output
            data['api'].say(args['channel'],
                'Lookup for IP: %s (%s)\n' % (answ['query'], answ['reverse']) +
                'ISP: %s(%s) - %s\n' % (answ['isp'], answ['org'], answ['as']) +
                'Country: %s (%s); Time zone: %s\n'%(answ['country'], answ['countryCode'], answ['timezone']) +
                # zipcode is always empty, but for the offchance that it isn't...
                'Region: %s(%s); City: %s; zipcode: %s\n' % (answ['regionName'], answ['region'], answ['city'], answ['zip']) +
                'Approx. location: %s %s \n' % (str(answ['lat']), str(answ['lon']))
            )
        else:
            data['api'].say(args['channel'], 'Query "' + answ['query'] + '" has failed with errmsg: ' + answ['message'])
