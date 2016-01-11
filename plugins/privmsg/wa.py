def main(data):
    if '!wa ' in data['recv']:
        import urllib
        from BeautifulSoup import BeautifulSoup
        args = argv('!wa',data['recv'])
        if args['argv'][1] == "-q":
            quietMode = True
            oQuery = ' '.join(args['argv'][2:])
        else:
            quietMode = False
            oQuery = ' '.join(args['argv'][1:])
        # URL escape query
        query = {'input': oQuery, 'appid': 'QPEPAR-TKWEJ3W7VA'}
        query = urllib.urlencode(query)
        baseUrl = 'http://api.wolframalpha.com/v2/query?'
        response = urllib2.urlopen(baseUrl + query).read()
        soup = BeautifulSoup(response)
        pods = soup.queryresult.findAll('pod')
        if pods and len(pods) >= 2:  # if we got an answer
            answers = []
            # Iterate the results
            for pod in pods:
                # Grab plaintext of the result
                answer = pod.subpod.plaintext.string
                if answer == None:                   
                    continue
                # Strip html entities from the response
                answer = html_decode(str(answer))
                for match in re.finditer(r"\\:([a-f|A-F|0-9]{4})", answer):
                    # Replace it with its corresponding Unicode character
                    try:
                        answer = answer.replace(
                            match.group(0),
                            unichr(int(match.group(1), 16))
                        )
                    except:
                        pass
                if type(answer) == unicode:
                    answer = answer.encode('utf-8')
                answers.append(answer)
            # Prepare these answers for IRC
            ircAnswersString = ""
            lines = '\n'.join(answers).splitlines()
            postShortLink = False
            if len(lines) > 5:
                lines = lines[:5]
                postShortLink = True
            if quietMode:
                lines = lines[:2]
                postShortLink = False
            for line in lines:
                if len(line) > 430:
                    ircAnswersString += "".join(line[:427]) + '...\n'
                else:
                    ircAnswersString += line + '\n'
            data['api'].say(args['channel'], ircAnswersString)
            if postShortLink:
                shortLink = maketiny("http://www.wolframalpha.com/input/?i=" + urllib.quote_plus(oQuery))
                data['api'].say(args['channel'], "More: " + shortLink)
        else:
            # We didn't get an answer, make cleverbot reply instead
            # Construct the string that makes the cleverbot plugin respond
            cleverBotFlag = data['config']['settings']['botNick'] + ":"
            # create a copy of data so we can modify it without affecting other scripts
            data2 = data.copy()
            # edit the new data variable to flag the cleverbot plugin
            data2['recv'] = data2['recv'].replace("!wa", cleverBotFlag)
            # emulate how cleverbot would have been run if invoked normally
            data['api'].runPlugin("cleverbot.py", "./plugins/privmsg/", data2)

        # kill plugin
        return None
