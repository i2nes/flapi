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


    def email(self):
        return self.key.id()

    def list_content(self):

        list_dict = {
            'email': self.key.id(),
            'links': [
                {
                    'rel': 'info',
                    'method': 'get',
                    'url': '{}/user/{}/info'.format(hostname, self.key.id()),
                },
            ],
        }

        return list_dict

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
                    'rel': 'info',
                    'method': 'get',
                    'url': '{}/user/{}/info'.format(hostname, self.key.id()),
                },
                {
                    'rel': 'delete',
                    'method': 'delete',
                    'url': '{}/user/{}/delete'.format(hostname, self.key.id()),
                },
                {
                    'rel': 'update',
                    'method': 'post',
                    'url': '{}/user/{}/update'.format(hostname, self.key.id()),
                    'parameters': {
                        'first_name': 'string',
                        'last_name': 'string',
                    },
                },
            ],
        }

        return content

