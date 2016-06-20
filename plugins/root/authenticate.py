def main(data):
    #:NickServ!NickServ@services. NOTICE TaiiwoBot :Taiiwo ACC 3
    args = argv(':', data['recv'])
    if args['nick'].lower() == "nickserv" and args['command'].lower() == "notice":
        msg_args = args['message'].split()
        for user in data['config']['settings']['userModes']:
            if msg_args[0] == user['nick']:
                if msg_args[2] == "3":
                    user['isAuth'] = 'True'
                else:
                    user['isAuth'] = 'False'
        saveConfigChanges(data['config'])
