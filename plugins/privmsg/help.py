def main(data):
    if "!help" in data['recv']:
        args = argv('!help', data['recv'])
        data['api'].say(args['channel'],
            "Plugin dictionary: http://tinyurl.com/lclasyv"
        )
