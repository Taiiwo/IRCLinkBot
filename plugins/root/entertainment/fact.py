def main(data):
	message = command("!fact", data['recv'])
	if str(message) != 'None':
		args = argv('!fact', data['recv'])
		return 'privmsg ' + args['channel'] + ' :' + textbetween("<strong>","</strong>", urllib2.urlopen("http://randomfunfacts.com").read())[3:-4] + '\r\n'

