def main(data):
        if '!r' in data['recv']:
                args = argv('!r', data['recv'])
                if 'd' in args['argv'][1] or 'D' in args['argv'][1]:
                        args['argv'][1].replace('D','d')
                        pos_of_d = re.search(r"[^a-zA-Z](d)[^a-zA-Z]", args['argv'][1]).start(1)
                        num_of_dice = args['argv'][1][:pos_of_d]
                        dice_value = args['argv'][1][pos_of_d + 1:]
                        try:
                                num_of_dice = int(num_of_dice)
                                dice_value = int(dice_value)
                                num_valid = True
                        except:
                                num_valid = False
                        if num_valid and num_of_dice >= 1 and len(str(num_of_dice)) <4 and len(str(dice_value)) < 10 and dice_value >= 1:
                                i = num_of_dice
                                total = 0
                                while i > 0:
                                        total += random.randint(1,dice_value)
                                        i = i - 1
                                return say(args['channel'],str(total))
                        else:
                                return ''
                else:
                        try:
                                int(args['argv'][1])
                                error = 0
                        except:
                                error = 1
                        if error != 1 and len(args['argv'][1]) < 10 and int(args['argv'][1]) >= 1:
                                print args['channel']
                                return 'PRIVMSG '+ args['channel'] +' :' + str(random.randint(1,int(args['argv'][1]))) + '\r\n'
