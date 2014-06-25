def main(self):
	if "!findphone" in data['recv']:
		args = argv("!findphone",data['recv'])
		number = args['argv'][1]
		if re.match('\d{9,11}',number):
			jsonres = urllib2.urlopen('https://api.opencnam.com/v2/phone/+' + str(number) + '?format=json&account_sid=ACe3213058aed64072b21c1aad690d10f5&auth_token=AU8d8f41d2a4ae42b09cd9356dc71db3b4').read()
			parsedjson = json.load(jsonres)
			tosend  = parsedjson['name'] + " "
			tosend += parsedjson['updated'] + " "
			tosend += parsedjson['price'] + " "
			tosend += parsedjson['created']
			return say(tosend,args['channel'])
