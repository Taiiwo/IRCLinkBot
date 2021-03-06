def main(data):
	url = geturl(data['recv'])
	args = argv(data['recv'])
	# if there is a url in a list of channels
	if args['channel'] in ["#cicadasolvers",] and url and args:
		import hashlib

		import libLinkScraper.gyazo
		import libLinkScraper.imgur
		import libLinkScraper.ppomf
		import libLinkScraper.bpaste
		import libLinkScraper.dpaste
		import libLinkScraper.infotomb
		import libLinkScraper.prntscrn
		import libLinkScraper.hastebin
		import libLinkScraper.pastebin
		import libLinkScraper.cubeupload
		
		archive_dir = os.environ['HOME'] + os.sep + "archive"
		archive_json = archive_dir + os.sep + "archive.json"

		timestamp = str(int(time() * 1000))
		paste_regex_to_func = {
			'^.*https?://pastebin\.com/[^ ]+': pastebin.get_content,
			'^.*https?://p\.pomf\.se/\d+': ppomf.get_content,
                        '^.*https?://(?:infotomb\.com)|(?:itmb\.co)/[0-9a-zA-Z]+': infotomb.get_content,
			'^.*https?://prntscr\.com/[0-9a-zA-Z]+': prntscrn.get_content,
			# dpaste doesnt get along with https, so we're not gonna bother
			'^.*http://dpaste\.com/[0-9a-zA-Z]+': dpaste.get_content,
			'^.*https?://bpaste\.net/(raw|show)/[0-9a-zA-Z]+': bpaste.get_content,
			'^.*https?://hastebin\.com/.+': hastebin.get_content,

			# here come the image hosters
			'^.*https?://(i\.)?cubeupload\.com/(im/)?[a-zA-Z0-9]+': cubeupload.get_content,
			'^.*https?://(i\.)?imgur\.com/(gallery/)?[a-zA-Z0-9]+': imgur.get_content,
			'^.*https?://(cache\.|i\.)?gyazo.com/[a-z0-9]{32}(\.png)?': gyazo.get_content
		}
		for regex, func in paste_regex_to_func.iteritems():
			if re.match(regex, url) is None:
				continue

			paste_data = func(url)

		# either no regex was found to match or no content could be pulled
		if not "paste_data" in locals() or paste_data is None:
			return

		paste_data['md5'] = hashlib.md5(paste_data['content']).hexdigest()
		paste_data['timestamp'] = timestamp
		final_folder = (
			archive_dir + os.sep + paste_data['site'])

		if not os.path.exists(final_folder):
			os.makedirs(final_folder)

		filename = str(timestamp) + "_" + paste_data['orig_filename']
		filename += ".%s" % paste_data['ext'] if paste_data['ext'] else ""

		file_location = final_folder + os.sep + filename
		paste_data['location'] = file_location

		with open(file_location, 'w') as f:
			f.write(paste_data['content'])

		del paste_data['content']

		with open(archive_json, "a+") as fj:
			try:
				dat = json.load(fj)
				dat.append(paste_data)
			except ValueError:
				dat = [paste_data]
		with open(archive_json, 'w+') as fj:
			json.dump(dat,fj)

		return

		if url:# if there's a url in something someone says
			log = {}
			log['url']         = url
			log['timestamp']     = timestamp
			log['poster']         = args['nick']
			log['fileLocation']     = "./archive/" + timestamp + fileExtension # need regex for this
			log['md5']        = hashlib.md5(contents.encode('utf-8')).hexdigest()
			logFile = open('archive.json', 'rw')
			logFile.write(json.dumps(json.loads(logFile.read()).append(log)))
"""
urls = [
    "http://gyazo.com/fc12a9bb2a4b92d1debef49b8279371f",
    "http://i.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png",
    "https://cache.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png",
#    "http://i.imgur.com/aChgMdG.gif",
#    "http://hastebin.com/zebihupixo.hs",
#    "http://hastebin.com/raw/zebihupixo",
#    "https://bpaste.net/show/31f01443d2b1",
#    "http://dpaste.com/03N0Y7Z",
#    "http://p.pomf.se/5504",
#    "http://pastebin.com/raw.php?i=gpRREVYd",
#    "http://prntscr.com/5o2enp",
#    "https://infotomb.com/y53jc",
]
for u in urls:
    main(u)
"""
