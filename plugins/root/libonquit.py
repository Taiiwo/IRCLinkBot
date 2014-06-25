#:nick!~ident@hostname QUIT :quitmessage
def main(data):
	if re.match('^:.*!.*@.*( QUIT :)',data['recv']):
		config = data['config']
		args = argv('@',data['recv'])
		for user in config['settings']['userModes']:
			if user['nick'] == args['user']:
				if user['isAuth'] == "True":
					user['isAuth'] == "False"
					saveConfigChanges(config)
		
