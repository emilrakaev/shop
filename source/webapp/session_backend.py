from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

from webapp.models import Basket


class SessionStore(DbSessionStore):
    def cycle_key(self):
        data = self._session
        key = self.session_key
        self.create()
        self._session_cache = data
        if key:
            Basket.update_session_key(key, self.session_key)
            self.delete(key)
