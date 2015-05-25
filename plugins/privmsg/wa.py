def main(data):
    if '!wa ' in data['recv']:
        import urllib
        from BeautifulSoup import BeautifulSoup
        args = argv('!wa',data['recv'])
        # Having to re-encode into UTF-8 because of ' '.join(). Thanks Obama.
        query = ' '.join(args['argv'][1:])
        # URL escape query
        query = {'input': query, 'appid': 'QPEPAR-TKWEJ3W7VA'}
        query = urllib.urlencode(query)
        baseUrl = 'http://api.wolframalpha.com/v2/query?'
        response = urllib2.urlopen(baseUrl + query).read()
        soup = BeautifulSoup(response)
        pods = soup.queryresult.findAll('pod')
        if pods and len(pods) >= 2:  # if we got an answer
            # Grab what they thought the question was (Interpretation)
            interp = pods[0].subpod.plaintext.string
            # Grab the answer to the question
            answer = pods[1].subpod.plaintext.string
            # Strip html entities from the response
            interp = html_decode(interp)
            answer = html_decode(answer)
            for match in re.finditer(r"\\:([a-f|A-F|0-9]{4})", answer):
                # Replace it with its corresponding Unicode character
                each = each.replace(
                    match.group(0),
                    unichr(int(match.group(1), 16))
                )
            # Iterate the interpretation and answer
            if len(answer) > 430:
                # upload to pastebin
                data = {
                    "api_dev_key": "00b92ae7e09af03e0eb077143ee24403",
                    "api_option": "paste",
                    "api_paste_name": interp,
                    "api_user_key": '',
                    "api_paste_code": interp + '\n' + answer
                }
                url = 'http://pastebin.com/api/api_post.php'
                pasteLink = urllib2.urlopen(url, data)
                data['api'].say(interp)
                data['api'].say(''.join(answer[0:430]))
                data['api'].say("More: " + pasteLink)
            else:
                for each in (interp, answer):
                    # Iterate each found instance of WA's Unicode escape format
                    # Send the result to the channel
                    data['api'].say(args['channel'], each)
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
