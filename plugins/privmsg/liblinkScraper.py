def main(data):
	url = geturl(data['recv'])
	if url:# if there's a url in something someone says
		timestamp = time.now()
		if re.match("^https?://infotomb\.com/.*$", url):
			paste_info = {
					'site': 'infotomb',
					'url': url,
				}
			response = requests.get(url)
			if response.status_code != 200:
				return
			m = re.match('^.*/([0-9a-zA-Z]+)(\.([a-zA-Z]+))?$',url)
			if not m.group(2):
				data = response.text
				soup = BeautifulSoup(data)
				url = soup.find_all('input')[2]['value']
				m = re.match('^.*/([0-9a-zA-Z]+)(\.([a-zA-Z]+))?$',url)
				if m:
					response = requests.get(url)
					if response.status_code != 200:
					return
				else:
					return 
				idd = m.group(3)
				paste_info['content'] = response.content
				paste_info['orig_filename'] = m.group(1)
				paste_info['extension'] = idd
			url = # code to download link
		if re.match("^https?://pomf\.se/.*$", url):
			url = # code to download link
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
