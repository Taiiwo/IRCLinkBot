def main(data):
	if '!scoop ' in data['recv']:
		args = argv("!scoop", data['recv']);
		if len(args['argv']) >= 2:
			queryStatus = False
			if args['argv'][1] != 'me':
				if modeCheck('a',data):
					queryStatus = True
				else:
					queryStatus = False
			else:
				queryStatus = True
			if queryStatus == True:
				try:
					ratio = int(args['argv'][3])
				except:
					ratio = 10
				url = args['argv'][2]
				scoop = urllib2.urlopen("http://thescoop.io/ots.php?to_sum="+ url +"&ratio=" + str(ratio)).read()
				scoop = html_decode(scoop)
				scoop = html_strip(scoop)
				scoop = " ".join(scoop.split())
				if args['argv'][1] == 'me':
					return say(args['nick'],scoop)
				else:
					return say(args['argv'][1], scoop)
