List of plugin commands for TaiiwoBot
=====================================
Plugins that don't require a command
------------------------------------
###LinkBot - This will post a title if:
- The link is not to the following filetypes: '.cgi','.CGI','.jpg','.png','.gif','.bmp'
TinyURL if:
- The link is longer than data['config']['settings']['maxLinkLen']
- The link has no title or is of invalid filetype
Both TinyURL and title if:
- The link is longer than data['config']['settings']['maxLinkLen']
- The link has a valid title and is not of invalid filetype
###CleverBot - Will open a cleverbot session on start up, and reply to any post mentioning
data['config']['settings']['botNick'] or data['config']['settings']['botNick'].lower()
(TaiiwoBot or taiiwobot, but not Taiiwobot, for example)
Plugins that require commands to initialize
###Whois on join - WHOIS scans every user that joins that has user modes
###Authenticate - Checks ALL WHOIS outputs for authentication
-------------------------------------------
| Name    	| Command	| Description					| Usage			| Example 			|
|:-------------:|:--------------|:----------------------------------------------|:----------------------|:------------------------------|

| Coinprice	| !coinprice	| Will fetch data from the BTC-e API		| [com] CUR1 CUR2	| !coinprice btc ltc		|

| FindIP	| !findip	| Searches an IP or hostname in the http://ip-api.com DB| [com] IP/hostname| !findip google.com		|

| LocateIP	| !locateip	| Uses the shodan library to  pull down a host scan from ShodanHQ DBs. Includes ports 80,21,22,161,5060 and a GeoIP. Only works if the IP has been scanned by shodan| [com] IP| !locateip 173.194.34.166|

| Love 		| !love		| Says "I love argv[1]"				| [com] argv[1]		| !love Taiiwo			|

| RFL		| !rfl		| Says "I really fucking love argv[1]"		| [com] argv[1]		| !rfl Taiiwo			|

| Wolfram Alpha	| !wa		| Returns the first plaintext string from the Wolfram Alpha API	| [com] multiword query	| !wa time in dubai|

| Wikipedia [DEV]| !wk		| Returns a short synapsis of a query from Wikipedia| [com] multiword query| !wk space time continuum	|

| List modes	| !listmodes	| Lists the bot modes for a user. At the time of Writing, the only two in use are 'a' and 'g' for Admin and Global respectively| [com] nick| !listmodes Taiiwo|

| 4chan search	| !4search	| Scans 4chan thread on a single board recursively for a word or phrase. Output in PM Maximum of 15 links. Using 'all' will take time and may get TaiiwoBot temporarily banned from the API if overused, so don't do that.| [com] board all/op word space-sep | !4search x op cicada |

| Fact		| !fact		| Gives a random fact from http://randomfunfacts.com| [com]		| !fact				|

| Joke		| !joke		| Parses the random joke page on sickipedia for jokes. subject to breakage when the site changes HTML format.| [com] | !joke	|

| Roll usage1	| !r		| Gives a simulated output of an argv[1] sided dice being rolled.| [com] argv[1]| !r 20			|

| Roll usage2	| !r		| Gives a sumulated output of an X sided dice being rolled Y times. 'd' stands for 'dice'| [com] XdY| !r 2d20|

| WYR	    	| !wyr		| Gets a random 'Would you rather?' question from http://rrrather.com| [com] | !wyr			|

Admin only plugins
------------------
###Requires +a in given channel or ga
| Name		| Command	| Description					| Usage			| Example 			|
|:-------------:|:--------------|:----------------------------------------------|:----------------------|:------------------------------|

| Auth me	| !authme	| Forces an authentication, needed when the bot Boots up after you log in.| [com]| !authme		|

| Join		| !join		| Joins a channel				| [com] channel		| !join #cicadasolvers		|

| Leave		| !leave	| Parts a channel				| [com] channel		| !leave #cicadasolvers		|

| Mode		| !mode		| Changes a user's/users' bot modes. '[]' is a binary option field. '()*' symbolises an argument that can be repeated infinitly| [com] ([+/-]MODE)* (nick )*| !mode +o-b Taiiwo Surtri|

| Send		| !send		| Enter an IRC command manaully. cannot run multiple commands| [com] command| !send privmsg Taiiwo :Nice Bot!|

| Say		| !say		| Sends a message to argv[1]. Can be channel or nick| [com] channel message | !say Taiiwo Nice Bot!	|
