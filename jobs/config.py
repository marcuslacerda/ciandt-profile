"""Config class."""
import os
import sys
sys.path.insert(1, os.path.abspath(os.curdir))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'lib'))

import logging
import yaml
from dotenv import load_dotenv

logger = logging.getLogger('profile')

# current_path = os.path.dirname(__file__)
resources_dir = os.path.join(os.path.expanduser('~'), '.resources')
dotenv_path = os.path.abspath(os.path.join(resources_dir, '.env'))
print 'resource dir: ' + resources_dir
if os.path.exists(dotenv_path):
    logger.debug('loading .env file')
    load_dotenv(dotenv_path)

class Config(object):
    """Operations for configuration class."""

    def __init__(self, resource_path=None, override=True):
        """Initializing config dictionary."""
        self.original_config = load_config(resource_path)
        self.override_config = {}
        if override:
            override_config(None, self.original_config, self.override_config)
        else:
            self.override_config = self.original_config

    def get(self, key):
        """Return value for key."""
        return self.override_config.get(key)


def load_config(resource_path=None):
    """Load resources/config.yaml file."""
    if not resource_path:
        resource_path = os.path.join(
            os.path.split(__file__)[0], "resources/config.yaml")

    with open(resource_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def override_config(context, config, new_config):
    """Loop each key from config and override with environment values."""
    for key, value in config.iteritems():
        key_upper = key.upper() if not context else '%s_%s' % (context, key.upper())
        if isinstance(value, dict):
            override_config(key_upper, value, new_config)
        else:
            value = os.environ.get(key_upper) or value
            # logger.debug('%s : %s' % (key_upper, value))
            new_config[key_upper] = value
