def main(data):
	message = command("!rfl", data['recv'])
	if str(message) != 'None':
		args = argv('!rfl', data['recv'])
		return 'privmsg ' + args['nick'] + ' :I really fucking love ' + str(message) + '\r\n'