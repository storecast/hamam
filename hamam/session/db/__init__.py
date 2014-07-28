from .models import db
from .store import DbSessionStore as SessionStore


DbSessionStore = SessionStore(db)
