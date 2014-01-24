def wyr(self,data):
	if "!wyr" in data['recv']:
		error = 1
		args = argv('!wyr',data['recv'])
		while error == 1:
			try:
				return 'PRIVMSG '+ args['channel'] +' :' + gettitle('http://www.rrrather.com/view/' + str(random.randint(0,40000)))+ '\r\n'
				error = 0
			except:
				print '[Server Error (Not my fault)]'
				error = 1

