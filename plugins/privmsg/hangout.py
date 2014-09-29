def main(data):
	run = False
	if '!g+' in data['recv']:
		args = argv('!g+', data['recv'])
		run = True
	elif '!G+' in data['recv']:
		args = argv('!G+', data['recv'])
		run = True
	if run:
		return say(args['channel'],'https://plus.google.com/hangouts/_/event/ch7k2ara9stvm6q0ubs7crkov9c')
