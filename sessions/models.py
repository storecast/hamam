from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class DjangoSession(db.Model):
    """Mapper class for django session model."""

    session_key = db.Column(db.String(40), primary_key=True)
    session_data = db.Column(db.Text())
    expire_date = db.Column(db.DateTime())

    def __init__(self, session_key, session_data, expire_date):
        self.session_key = session_key
        self.session_data = session_data
        self.expire_date = expire_date
