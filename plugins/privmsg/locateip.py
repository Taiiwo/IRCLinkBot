def main(data):
    if '!locateip' in data['recv']:
        try:
            from shodan import WebApi
        except:
            print "[E] Shodan not installed"
            return
        args = argv('!locateip',data['recv'])
        try:#if shodan is installed (sudo pip install shodan)
            api = WebAPI("KpYC07EoGBtGarTFXCpjsspMVQ0a5Aus")#don look
            query = args['argv'][1]
            socket.inet_aton(query)
        except socket.error:
            return None
        results = api.host(query)
        output = []
        output.append('OS: ' + str(results['os']))
        output.append('City: ' + str(results['city']) + '\tPostal code: ' + str(results['postal_code']))
        output.append('Area code: ' + str(results['area_code']) + '\t\tCountry code: ' + str(results['country_code']))
        output.append('Region name: ' + str(results['region_name']) + '\tCountry name: ' + str(results['country_name']))
        output.append('Latitude: ' + str(results['latitude']) + '\tLongitude: ' + str(results['longitude']))
        ports = []
        for data in results['data']:
            port = data['port']
            if not str(port) in ports:
                ports.append(str(port))
        output.append('Open ports: ' + ', '.join(ports))
        ircoutput = ''
        for line in output:
            ircoutput += say(args['channel'],line)
        return ircoutput
