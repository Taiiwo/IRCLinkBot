def main(data):
	if ':End of /WHOIS list.' in data['recv']:
                args = argv("", data['recv'])
                if ':is logged in as' in data['recv']:
                        lastline = data['recv'].splitlines()[len(data['recv'].splitlines())-1]
                        supposedNick = textbetween(data['nick']+' ',' :End of /WHOIS list.',lastline)
			data['config']['settings']['userModes'][user['nick']]['isAuth'] = 'False'
			for user in data['config']['settings']['userModes']:
				if supposedNick == user['nick']:
					data['config']['settings']['userModes'][user['nick']]['isAuth'] = 'True'
			saveConfigChanges(data['config'])
				
				
