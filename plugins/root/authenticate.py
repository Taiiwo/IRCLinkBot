def main(data):
	if ':End of /WHOIS list.' in data['recv']:
                args = argv("", data['recv'])
                if ':is logged in as' in data['recv']:
                        lastline = data['recv'].splitlines()[len(data['recv'].splitlines())-1]
                        supposedNick = textbetween(data['config']['settings']['botNick']+' ',' :End of /WHOIS list.',lastline)
			for user in data['config']['settings']['userModes']:
				if supposedNick == user['nick']:
					user['isAuth'] = 'True'
		else:
			lastline = data['recv'].splitlines()[len(data['recv'].splitlines())-1]
                        supposedNick = textbetween(data['config']['settings']['botNick']+' ',' :End of /WHOIS list.',lastline)
			for user in data['config']['settings']['userModes']:
                                if supposedNick == user['nick']: 
					user['isAuth'] = 'False'
		saveConfigChanges(data['config'])				
				
