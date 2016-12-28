"""Config class."""
import logging
import yaml
import os.path
import os
from dotenv import load_dotenv

logger = logging.getLogger('stack')

# current_path = os.path.dirname(__file__)
resources_dir = os.path.join(os.path.expanduser('~'), '.resources')
dotenv_path = os.path.abspath(os.path.join(resources_dir, '.env'))
if os.path.exists(dotenv_path):
    logger.debug('loading .env file')
    load_dotenv(dotenv_path)

class Config(object):
    """Operations for configuration class."""

    def __init__(self, resource_path=None):
        """Initializing config dictionary."""
        self.original_config = load_config(resource_path)
        self.override_config = {}
        override_config(None, self.original_config, self.override_config)

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
