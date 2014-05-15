import base64
from datetime import datetime
import json
import os
import re
import tempfile
import unittest
from app import app
from sessions.models import db, DjangoSession


class SessionViewTestCase(unittest.TestCase):

    session_id = 'some id'
    session_data = json.dumps({'foo': 'bar'})

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % app.config['DATABASE']
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_no_cookie_data(self):
        """Shared session view returns empty response
        if there is no cookies.
        """
        rv = self.client.get('/session/')
        self.assertEqual('{}', rv.data)

    def test_content_type(self):
        """Shared session view returns correct
        `Content-Type` header.
        """
        rv = self.client.get('/session/')
        self.assertEqual('application/json', rv.content_type)

    def test_session_id_in_db(self):
        """Shared session view returns correct session data."""
        self.create_session()
        with self.client as c:
            c.set_cookie('*', app.config['SESSION_COOKIE_NAME'], self.session_id)
            rv = c.get('/session/')
            self.assertEqual(self.strip_line(self.session_data), self.strip_line(rv.data))

    def test_session_id_not_in_db(self):
        """Shared session view returns empty response
        if the session not in the db.
        """
        with self.client as c:
            c.set_cookie('*', app.config['SESSION_COOKIE_NAME'], self.session_id)
            rv = c.get('/session/')
            self.assertEqual('{}', rv.data)

    def create_session(self):
        """Helper that puts the session in the database."""
        # make session look django-ish
        session = DjangoSession(self.session_id, base64.b64encode(bytes('hash:%s' % self.session_data)), datetime.now())
        with app.app_context():
            db.session.add(session)
            db.session.commit()

    def strip_line(self, line):
        """Helper that strips all the whitespaces from the given string.

        :param line: string to strip
        :type line: str or unicode
        :return: stripped string
        :rtype: str or unicode
        """
        return re.sub(r'\s+', '', line)


if __name__ == '__main__':
    unittest.main()
