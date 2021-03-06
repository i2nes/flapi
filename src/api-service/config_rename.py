# Flask App Configurations
# This is an example config file. Create a config.py with your own secrets.
import os
from socket import gethostname


config = {
    'DEBUG': True if os.getenv('SERVER_SOFTWARE', '').startswith('Development/') else False,
    'SECRET_KEY': 'Some big sentence',
}

http_security = 'http' if config['DEBUG'] else 'https'
hostname = '{}://{}'.format(http_security, gethostname())