def main(data):
        #:Taiiwo!~Taiiwo@cpc3-nott16-2-0-cust414.12-2.cable.virginm.net JOIN ##426699k
        if ' JOIN ' in data['recv']:
                args = argv('JOIN', data['recv'])
		regdNick = False
		for user in data['config']['settings']['userModes']:
			if args['nick'] == user['nick']:
				regdNick = True
		if regdNick:
                	data['api'].say('nickserv', 'acc ' + args['nick'])

