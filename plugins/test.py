class Plugin():
    def __init__(self, bot):

        @bot.on("message")
        def on_message(message):
            print(message)
