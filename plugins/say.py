def main(data):
	if '!say' in data['recv']:
		print "executing"
		return 'PRIVMSG #426699t :Test\r\n'
