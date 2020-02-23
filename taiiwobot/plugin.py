class Plugin:
    def unload(self):
        if hasattr(self, "interface"):
            self._unloaded = True
            del self.interface

    def mention(self, user):
        return user

    def code_block(self, text):
        return text
