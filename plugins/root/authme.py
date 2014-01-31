def main(data):
    if '!authme' in data['recv']:
        args = argv('!authme', data['recv'])
        return "WHOIS " + args['nick']