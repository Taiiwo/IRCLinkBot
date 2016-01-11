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
                                def sumLink(url, ratio):
				    scoop = urllib2.urlopen("http://phantas.ml/ots/?to_sum="+ url +"&ratio=" + str(ratio)).read()
				    scoop = html_decode(scoop)
				    scoop = html_strip(scoop)
				    scoop = " ".join(scoop.split())
                                    return scoop
				if len(args['argv']) == 4 and args['argv'][3].isdigit():
					ratio = args['argv'][3]
				else:
					ratio = 10
				url = args['argv'][2]
				if args['argv'][1] == 'me':
                                        scoop = sumLink(url, ratio)
					return say(args['nick'],scoop)
				else:
                                        if args['argv'][1][0] == "#":
                                            while 1:
                                                scoop = sumLink(url, ratio)
                                                if len(scoop) < 280:
                                                    break
                                                else:
                                                    ratio -= 5
					return say(args['argv'][1], scoop)
