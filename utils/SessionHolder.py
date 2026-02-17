import aiohttp

# --- Improved Session Management ---
# This keeps one connection pool open for your whole app
class PersistentSession:
    session: aiohttp.ClientSession = None

    def get_session(self):
        return self.session