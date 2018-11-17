from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash, check_password_hash
from config import hostname


class User(ndb.Model):

    # User(id=email)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    password = ndb.StringProperty()
    isAdmin = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def content(self):

        content = {
            'email': self.key.id(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'isAdmin': self.isAdmin,
            'created': self.created,
            'updated': self.updated,
            'links': [
                {
                    'rel': 'self',
                    'method': 'get',
                    'url': '{}/user/{}'.format(hostname, self.key.id()),
                },
                {
                    'rel': 'delete',
                    'method': 'delete',
                    'url': '{}/user/{}'.format(hostname, self.key.id()),
                },
                {
                    'rel': 'update',
                    'method': 'post',
                    'url': '{}/user/{}'.format(hostname, self.key.id()),
                    'parameters': {
                        'first_name': 'string',
                        'last_name': 'string',
                    },
                },
            ],
        }

        return content

