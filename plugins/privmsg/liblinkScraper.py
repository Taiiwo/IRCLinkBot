def main(data):
	url = geturl(data['recv'])
	if url:# if there's a url in something someone says
		import urlLurker
		timestamp = time.now()
		if re.match("^https?://infotomb\.com/.*$", url):
			url = urlLurker.infotomb(url)
		if re.match("^https?://pomf\.se/.*$", url):
			url = urlLurker.pomf(url)
		# download file
		contents = urllib2.urlopen(url).read()
		file = open('./archive/' + timestamp + fileExtension, 'rw')
		file.write(contents)
		# log data on file to a log
		args = argv(data['recv'])
		log = {}
		log['url'] 		= url
		log['timestamp'] 	= timestamp
		log['poster'] 		= args['nick']
		log['fileLocation'] 	= "./archive/" + timestamp + fileExtension# need regex for this
		log['md5']		= hashlib.md5(contents.encode('utf-8')).hexdigest())
		logFile = open('archive.json', 'rw')
		logFile.write(json.dumps(json.loads(logFile.read()).append(log)))
