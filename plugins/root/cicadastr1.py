def main(data):
	global TwitterSearchThread
	if not "TwitterSearchThread" in globals():
		TwitterSearchThread = True
		def loop():
			import twitter
			global s
			while 1:
				twitterAuth = json.loads(open('./auth.include', 'r').read())
				twApi = twitter.Api(
						consumer_key =  twitterAuth['consumerKey'   ],
						consumer_secret =   twitterAuth['consumerSecret'                ],
						access_token_key =  twitterAuth['accessTokenKey'                ],
						access_token_secret =   twitterAuth['accessTokenSecret' ])
				ctweet = twApi.GetUserTimeline(screen_name = '1231507051321' , count=200)
				count=0
				for i in ctweet:
					if re.match('.*2015$', i.created_at):
						count+=1
				if count>0:
					s.send( say("#cicadasolvers" , str(count) + ' new tweet(s): "' + str(ctweet[0].text) + '" - ' + maketiny("https://twitter.com/1231507051321/status/" + str(ctweet[0].id))))
					s.send( say("Taiiwo" , str(count) + ' new tweet(s): "' + str(ctweet[0].text) + '" - ' + maketiny("https://twitter.com/1231507051321/status/" + str(ctweet[0].id))))
					s.send( say("Killjoy", str(count) + ' new tweet(s): "' + str(ctweet[0].text) + '" - ' + maketiny("https://twitter.com/1231507051321/status/" + str(ctweet[0].id))))
					break
				time.sleep(30)
		thread.start_new_thread(loop, ())

