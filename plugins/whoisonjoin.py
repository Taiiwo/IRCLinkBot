def main(data):
        #:Taiiwo!~Taiiwo@cpc3-nott16-2-0-cust414.12-2.cable.virginm.net JOIN ##426699k
        if ' JOIN ' in data['recv']:
                args = argv('JOIN',data['recv'])
                return 'WHOIS ' + args['nick'] + '\r\n'

