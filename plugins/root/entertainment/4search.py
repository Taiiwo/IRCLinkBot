def main(data):
	if '!4search' in data['recv']:
		args = argv('!4search',data['recv'])
		if args['argv'][1] == 'usage':
			return say(args['channel'], '!4search [board] [op/all] [query ("-" = Spaces)]')
		board = args['argv'][1]
		arg = args['argv'][2]#Should be either all or op
		words = args['argv'][3:]
		#Doing stupid TJ's suggestion:
		for word in words:
			for letter in word:
				if letter == '-':
					letter = ' '
		results = []
		rawjson = urllib2.urlopen('http://api.4chan.org/' + board + '/catalog.json').read()
		time.sleep(1)
		parsedjson = json.loads(rawjson)
		count = 0
		pagecount = 0
		retme = []
		for page in parsedjson:
			print 'Searching page ' + str(count)
			count += 1
			threadcount = 0
			for thread in page['threads']:
				if 'args' in locals():
					if arg != 'op':
						print 'On thread ' + str(threadcount)
						threadcount += 1
						#get thread number
						num = thread['no']
						try:
							rawreplies = urllib2.urlopen('http://api.4chan.org/' + board + '/res/' + str(num) + '.json').read()
						except:
							print "Thread 404'd"
							break
						time.sleep(0.00001)
						parsedreplies = json.loads(rawreplies)
						for post in parsedreplies['posts']:
							if 'com' in post:
								for string in words:
									if string in post['com']: # (Thinking of checking post['name']
										if num == post['no']:
											retme.append('http://boards.4chan.org/' + board + '/res/' + str(num))
											print 'http://boards.4chan.org/' + board + '/res/' + str(num)
										else:
											retme.append('http://boards.4chan.org/' + board + '/res/' + str(num) + '#p' + str(post['no']))
											print 'http://boards.4chan.org/' + board + '/res/' + str(num) + '#p' + str(post['no'])
					else:
						#print pagecount
						pagecount += 1
						if 'com' in thread:
							for string in words:
								if string in thread['com']:
									retme.append('http://boards.4chan.org/' + board + '/res/' + str(thread['no']))
									print 'http://boards.4chan.org/' + board + '/res/' + str(thread['no'])
		if retme == []:
			return say(args['nick'], "No threads found")
		retmeforrealthistime = []
		lt = 15
		appendloop = 0
		for i in retme:
			if appendloop <= lt:
				retmeforrealthistime.append(say(args['nick'], i))
			appendloop += 1
		return ''.join(retmeforrealthistime)
