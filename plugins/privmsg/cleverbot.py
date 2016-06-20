def main(data):
    if data['config']['settings']['botNick'] in data['recv']\
            or data['config']['settings']['botNick'].lower() in data['recv']:
        from cleverbot import Cleverbot
        global cleverbot
        if not 'cleverbot' in globals():  # check for instance
            cleverbot = Cleverbot()
            # print "making new bot"
        args = argv('', data['recv'])
        query = args['message']
        query = query.replace('\n','')
        query = query.replace('\r','')
        query = query.replace(data['config']['settings']['botNick'] + ':','')
        query = query.replace(data['config']['settings']['botNick'],'CleverBot')
        answer = html_decode(cleverbot.ask(query))
        answer = answer.replace('CleverBot',data['config']['settings']['botNick'])
        answer = answer.replace('Cleverbot',data['config']['settings']['botNick'])
        answer = answer.replace('God','Taiiwo')
        answer = answer.replace('god','Taiiwo')
        debug = 'Query: ' + query + ' -- Answer: "' + answer + '"'
        print debug

        data['api'].say(args['channel'], args['nick'] + ': ' + answer)
