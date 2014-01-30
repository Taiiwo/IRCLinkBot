def main(data):
	from datetime import datetime
	if '!coinprice ' in data['recv']:
		args = argv('!coinprice', data['recv'])
		cur1 = args['argv'][1].upper()
		cur2 = args['argv'][2].upper()
	        while 1:
	        	try:
	                	jsondata = urllib2.urlopen("https://btc-e.com/api/2/" + cur1.lower() + "_" + cur2.lower() +  "/ticker").read()
	                	break
	            	except:
	                	time.sleep(5)
		prices = json.loads(jsondata)
		try:
			prices['error']
			return False
		except:
			pass
		if prices:# should never be false.
			ticker = prices['ticker']
			timeDiff = data['config']['settings']['hoursDiffGMT']
			if timeDiff[0] == '-':
				timeDiff = abs(int(timeDiff[1:])*60*60)
			elif timeDiff[0] == '+':
				timeDiff = int(timeDiff[1:])*60*60
			time = datetime.fromtimestamp(int(ticker['updated'] - timeDiff)).strftime('%Y-%m-%d %H:%M:%S')
			delay = int(ticker['server_time']) - int(ticker['updated'])
			delay = datetime.fromtimestamp(delay - timeDiff + 3600).strftime('%H:%M:%S')
			r = "High: %s%s Low: %s%s Last Trans: %s%s Time: %s Delay: %s"%(ticker['high'],cur2,ticker['low'],cur2,ticker['last'],cur2,time,delay)
			return say(args['channel'],r)
