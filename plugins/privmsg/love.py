def main(data):
    message = command("!love",data['recv'])
    if str(message) != 'None':
        args = argv('!love', data['recv'])
        return say(args['channel'],'I love ' + str(message))# Example of 'say' function.
