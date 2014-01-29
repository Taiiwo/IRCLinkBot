def main(data):
        args = argv('@',data['recv'])
	#look for URL
	try:
		link = geturl(data['recv'])[0]
	except:
		link = False
	if link and link != '':
		#look for title
		badext = ('.cgi','.CGI','.jpg','.png','.gif','.bmp')
		if not link[-4:] in badext:
			title = gettitle(link)
			if title:
				title = title.replace('\n',' ')
				if len(title) >= 150:
					title = title[:150]
				title = html_decode(title)
				title = title.encode('ascii', 'ignore')
				if len(link) > int(data['config']['settings']['maxLinkLen']):
					#post title + tiny
					return say(args['channel'], '^ ' + title + ' ' + maketiny(link) + ' ^')
				else:
					#post title only
					return say(args['channel'], '^ ' + title + + ' ^')
		if len(link) > int(data['config']['settings']['maxLinkLen']):
			#post tiny only
			return say(args['channel'], '^ ' + maketiny(link) + ' ^')
		else:
			#nothing
			return False
