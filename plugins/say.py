def main(data):
	args = argv("!say", data['recv'])
	if args['argv'][0] == '!say' and args['nick'] in self.authnick:
		say = ' '.join(args['argv'][2:])
		return 'privmsg ' + args['argv'][1] + ' :' + say + '\r\n'
