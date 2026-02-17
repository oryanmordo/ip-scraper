import aiohttp

class PersistentSession:
    session: aiohttp.ClientSession = None

    def get_session(self):
        return self.session