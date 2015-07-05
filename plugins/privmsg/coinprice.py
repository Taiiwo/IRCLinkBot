def main(data):
    from datetime import datetime
    import time
    import urllib
    if '!coinprice ' in data['recv']:
        args = argv('!coinprice', data['recv'])
        cur1 = args['argv'][1].lower()
        cur2 = args['argv'][2].lower()
        requestUrl = "https://btc-e.com/api/2/%s_%s/ticker" % (
            urllib.quote_plus(cur1),# make sure the string is
            urllib.quote_plus(cur2)# encoded, before sending it
        )
        jsondata = urllib2.urlopen(requestUrl).read()
        prices = json.loads(jsondata)
        if 'error' in prices:
            data['api'].say(args['channel'], "No such conversion")
        if prices:# should never be false.
            ticker = prices['ticker']
            timeDiff = data['config']['settings']['hoursDiffGMT']
            if timeDiff[0] == '-':
                timeDiff = -int(timeDiff[1:])*60*60
            elif timeDiff[0] == '+':
                timeDiff = int(timeDiff[1:])*60*60
            time = datetime.fromtimestamp(int(ticker['updated'] - timeDiff))
            time = time.strftime('%d-%m-%y %H:%M:%S')
            delay = int(ticker['server_time']) - int(ticker['updated'])
            delay = datetime.fromtimestamp(delay - timeDiff + 3600)
            delay = delay.strftime('%H:%M:%S')
            if str(delay) == '00:00:00':
                delay = '0'
            r = "High: %s%s " \
                "Low: %s%s "\
                "Avg: %s%s "\
                "Last Trans: %s%s "\
                "Time: %s "\
                "Delay: %s" % (
                    ticker['high'],
                    cur2,
                    ticker['low'],
                    cur2,
                    ticker['avg'],
                    cur2,
                    ticker['last'],
                    cur2,
                    time,
                    delay
                )
            data['api'].say(args['channel'], r)
        else:
            data['api'].say(args['channel'], "Unspecified error from server")
