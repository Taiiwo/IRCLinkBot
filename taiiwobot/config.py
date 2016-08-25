import json
from . import irc

def get_config():
    config_location = "config.json"
    default_config = {
        "server_config": {
            "host": "example.com",
            "user": "TaiiwoBot",
            "nick": "TaiiwoBot",
            "autojoin": []
        }
    }
    try:
        user_config = json.loads(open(config_location).read())
    except (IOError, OSError):
        answer = input(
            "No config file was found. Would you like to generate one? (y/N)"
        )
        if answer != "" and answer[0].lower() == "y":
            open(config_location, "w+").write(json.dumps(default_config, indent=4))
            print("[i] A config file was created. Edit it and re-run.")
        else:
            print("[i] A config file is required to run TaiiwoBot")
        quit()
    default_config.update(user_config)
    return default_config
