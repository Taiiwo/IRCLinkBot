# Find IP plugin for Taiiwobot by zingmars
# All maintaining duties still go to Taiiwo
# This plugin was tested on the live session of Taiiwobot, and it crashed TaiiwoBot   1   times during dev. (wasn't my fault, I swear)
def main(data):
    if '!findip ' in data['recv']:
        args = argv('!findip',data['recv'])
        
		# GET whois data
        query = ' '.join(args['argv'][1:] )
        import urllib
        query = urllib.quote(query)
        try:
            whois = urllib2.urlopen('http://ip-api.com/json/' + query) # This service can take up to 14k requests per hour. Try not to overuse it.
            answ = json.load(whois)
        except:
            return say( args['channel'], 'API Error.' ) 
        
        # Mad error handling skills (from coinprice plugin)
        try:
			if answ == False: # Closest I could find to checking for null
			    return say( args['channel'], 'General JSON failure.' )
        except:
			pass        
        
        output = []
        if answ['status']  == 'success':
            # Reverse IP lookup
            try:
                reverse = urllib2.urlopen('http://restdns.net/' + query + '/x') # Sadly ip-api only provides reverse IP lookup through their website
                answ2 = json.load(reverse)
                answ2 = ''.join(answ2['PTR'])
            except:
                answ2 = query
                
            # prepare output     
            output.append( say( args['channel'], 'Lookup for IP: ' + answ['query'] + ' (' + answ2 + ')\n' ) )
            output.append( say( args['channel'], 'ISP: ' + answ['isp'] + '(' + answ['org'] + ') - ' + answ['as'] + '\n' ) )
            output.append( say( args['channel'], 'Country: ' + answ['country'] + ' (' + answ['countryCode'] + '); Time zone: ' + answ['timezone'] + '\n' ) )
            output.append( say( args['channel'], 'Region: ' + answ['regionName'] + '(' + answ['region'] + ')' + '; City: ' + answ['city'] + '; zipcode: ' + answ['zip'] + '\n' ) ) # zipcode is always empty, but for the offchance that it isn't...
            output.append( say( args['channel'], 'Approx. location: ' + str(answ['lat']) + ' ' + str(answ['lon']) + '\n' ) )
        else:
            output.append( say( args['channel'], 'Query "' + answ['query'] + '" has failed with errmsg: ' + answ['message'] ) )
        
        # output
        return ''.join(output)
