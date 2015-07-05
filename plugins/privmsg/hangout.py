def main(data):
    args = False
    coms = ["!G+", "!g+"]
    for com in coms:
        if com in data['recv']:
            args = argv(com, data['recv'])
            break
    if args:
        return say(args['channel'],
            'https://plus.google.com/'\
            'hangouts/_/event/ch7k2ara9stvm6q0ubs7crkov9c'
        )
