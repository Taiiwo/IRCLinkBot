IRCLinkBot(TaiiwoBot) v4
==========
Introduction - What is IRCLinkBot(TaiiwoBot) v4?
------------------------------------------------
This program is mainly a core IRC bot, that allows you to add custom plugins and customization options that runs quickly on a high memory system.
There are a lot of plugins preinstalled that I developed. 
In fact, the whole bot is in functioning condition.
The latest version of this bot is running unedited on my server, so you may run into it on IRC.

Introduction - What is Version 4? Why is it better than Version3?
-----------------------------------------------------------------
In this restructure, I tried to make the bot both easy to develop, and also add more flexibility with regards to creating output data.

I wanted to have individual plugin files with a simple interface, to make it easy for developers to make quick plugins, and not have them do too much work to run them.
I also wanted to have the bot update automatically, with regards to both the config, and developing plugins.

 - Plugins will be executed in respose to certain actions, as opposed to every time a message is received from IRC.
 - Plugins will be executed in separate threads separated by directory.

How to run the bot:
-------------------
You will need the following libraries (Listed by their names in the debian repositories):
 - python-BeautifulSoup

As mentioned before, the bot is running in it's current configuration.
This means you'll need to change linkbot.conf.
Linkbot.conf is well commented, so that should walk you through the editing process.

Once you have the config setup, you'll need to choose your plugins.
Some plugins come preinstalled with TaiiwoBot, these cover a wide range of things, but feel free to disable them and add your own.
(all plugins are ran within a 'try' statement, so there is no danger of crashing the bot with your experiments (Beware, however, of channel flooding))
You can disable plugins by adding a '#' to the end of their filename.
To disable wa.py for example (In /plugins/privmsg/information) type in the directory of wa.py(In *NIX): ```mv wa.py wa.py\#```

Now you're ready to boot up TaiiwoBot!
Simply type: python main.py
Note, you can add an ' &' at the end of the command in order to daemonize TaiiwoBot (To keep your shell while he's running( TaiiwoBot is male and sentient ;) ))
Note note, you should disable the output options of TaiiwoBot in the config file if you are to do this.

Developing Plugins
------------------
### The Plugin Code
The main() function of the plugin will be run.
Feel free to import external libraries in your plugin (Duplicate importations are handled by Python).
main() is run as: main(data)
where data is an  associative array (Dict) containing data from the bot.
It is done in this way so that I can continuously offer new information to the plugin developers without losing compatability with old plugins.
It is because of this however, that it's difficult to keep the documentation up to date.
If you want to take a look at what is definitely being passed inside data, I reccomend you have a read through main.py
Otherwise, here is a list of the most useful information passed inside data:

data['recv'] - This contains the latest data pulled from IRC, delivered in a maximum size specified by 'recvLen' in the config.
	For examples of output, check the logs (If logging is enabled)
data['config'] - This is a JSON DOM, parsed from the config file.
	This DOM is updated every time a new message is sent, so there is no need to manually reimport it.
	You can change it with updateConf(data['config']).
	This will write any changes you have made to the physical file.
	This is recomended if you ever change the data, as un'updated' data will not be present when the bot is rebooted. 
data['loop'] - This is simply the amount of messages received from IRC.

The only other important(restrictive) thing is what to return.
Each plugin must return a string, '', None, , False, or just not return anything (You theoretically could return an integer. It would be converted to a string, but I don't see why you'd want to, as there are no integer only IRC commands)
You're most likely going to want to try to return a string as a result of a positive plugin run.
Simply, anything returned by a plugin is sent to IRC.
Not so simply, you are responsible for appending '\r\n' to each individual command.
If you want to send multiple commands (Such as multiline speech), you need only separate the commands with '\r\n'.
For example:
```Python
def main(data):
	return 'PRIVMSG Taiiwo :Nice bot.\r\nPRIVMSG Taiiwo :I like the part where you make your own plugins.\r\n'

```

### Plugin Placement
One of the 2 main ways that TaiiwoBot boast speed, is because his plugins are ran situationally.
Most IRC bots simply run every plugin for every received message from IRC.
TaiiwoBot, on the other hand, uses the plugins location to determine when the plugin is run. so, for example, your plugins waiting for a command via private message to itself, aren't run until the bot receives a private message addressed to itsself.
Simularly, the plugins that you intend to run in response to things said in channels (Usually a vast majority of them), aren't executed on, say 'PING' requests.

The structure is fairly simple. Below is a commented directory tree.

| dir name 		| description |
|-----------------------|-------------|
| /plugins/root/	| Python files placed here will have main() executed when ever a message is received from IRC. |
| /plugins/privmsg/	| Python files placed here will have main() executed when a private message is sent to one of the channels that TaiiwoBot has joined. |
| /plugins/privmsgbot/	| These scripts will have main() executed whenever TaiiwoBot receives a private message is send directly to TaiiwoBot (/msg TaiiwoBot !help) |

All new folders with these directories will we dropped into, and all plugins within them will be executed in separate threads.
This allows you to separate plugins by speed, or by category, or however you'd like.
You can ignore a directory by prepending '#' to it's name.
This is useful for quickly disabling large groups of plugins.

TaiiwoBot was designed to have a massive amount of plugins running at once.
Adding more plugins only uses more memory and does not slow down response time (As long as your server can handle the concurrent processing) as all plugins are executed in threads separated by directory.
TaiiwoBot does not wait for a single plugin to finish before running the next.
