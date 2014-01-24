def main(data):
        if '!join' in data['recv']:
                args = argv('!join',data['recv'])
                if args['nick'] in self.authnick:
                        return 'JOIN ' + args['argv'][1] + '\r\n'
