def main(data):
        args = argv('@',data['recv'])
	#look for URL
	link = geturl(data['recv'])
	if link and link != "" and not modeCheck('b',data):
		link = link[0]
		#look for title
		badext = ('.cgi','.CGI','.jpg','.png','.gif','.bmp')
		if not link[-4:] in badext:
			title = gettitle(link)
			if title:
				title = title.replace('\n',' ')
				title = title.replace('\r',' ')
				if len(title) >= 150:
					title = title[:150]
				title = title.encode('ascii', 'ignore')
				title = html_decode(title)
				title = " ".join(title.split())
				if len(link) > int(data['config']['settings']['maxLinkLen']):
					#post title + tiny
					return say(args['channel'], '^ ' + title + ' ' + maketiny(link) + ' ^')
				else:
					#post title only
					return say(args['channel'], '^ ' + title + ' ^')
		if len(link) > int(data['config']['settings']['maxLinkLen']):
			#post tiny only
			return say(args['channel'], '^ ' + maketiny(link) + ' ^')
		else:
			#nothing
			return False
