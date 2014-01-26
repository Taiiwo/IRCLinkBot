import re
def main(data):
	if '!mode' in data['recv']:
		if modeCheck('a', data):
			args = argv('!mode', data['recv'])
			modes = args['argv'][1]
			nicks = args['argv'][2:]
			userExists = 0
			for user in data['config']['settings']['userModes']:
				if user['nick'] in nicks:
					for mode in re.findall('..',''.join(modes)):# for each 2 letters in modes
						if mode[0] == '-':
							if mode[1] in user['modes']:
								userModesString = str(user['modes'])
								print userModesString
								userModesString = userModesString.replace(mode[1],'')
								print userModesString
								user['modes'] = userModesString
								userExists += 1
								
						elif mode[0] == '+':
                        	                	if not mode[1] in user['modes']:
								user['modes'] += mode[1]
			if userExists < len(nicks):
				for nick in nicks:
					reg = 0
					for user in data['config']['settings']['userModes']:
						if user['nick'] == nick:
							reg = 1
					if reg == 0:
						newUser = {}
						newUser['nick'] = nick
						newUser['channel'] = args['channel']
						newUser['isAuth'] = 'False'
						addModes = ''
						for mode in re.findall('..',''.join(modes)):
							if mode[0] == '+':
								addModes += mode[1]
						newUser['modes'] = addModes
						data['config']['settings']['userModes'].append(newUser)
			saveConfigChanges(data['config'])
					
