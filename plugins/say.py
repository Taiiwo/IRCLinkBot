def main(data):
	if '!say' in data['recv']:
		args = argv("!say", data['recv'])
		if args['nick'] in self.authnick:
			say = ' '.join(args['argv'][2:])
			return 'privmsg ' + args['argv'][1] + ' :' + say + '\r\n'
