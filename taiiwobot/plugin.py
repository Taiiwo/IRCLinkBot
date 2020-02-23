class Plugin:
    def unload(self):
        if hasattr(self, "interface"):
            self._unloaded = True
            del self.interface
