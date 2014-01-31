def main(data):
	if '!send ' in data ['recv'] and modeCheck('a', data):
		args = argv('!send', data['recv'])
		return ' '.join(args['argv'][1:]) + '\r\n'
