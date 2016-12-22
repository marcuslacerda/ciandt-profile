"""Config class."""
import yaml
import os.path
import os
from dotenv import load_dotenv

current_path = os.path.dirname(__file__)
dotenv_path = os.path.abspath(os.path.join(current_path, '.env'))
print dotenv_path
load_dotenv(dotenv_path)

class Config(object):
    """Operations for configuration class."""

    def __init__(self):
        """Initializing config dictionary."""
        self.original_config = load_config()
        self.override_config = {}
        override_config(None, self.original_config, self.override_config)

    def get(self, key):
        """Return value for key."""
        return self.override_config.get(key)


def load_config():
    resource_path = os.path.join(os.path.split(__file__)[0], "resources/config.yaml")
    with open(resource_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def override_config(context, config, new_config):

    for key, value in config.iteritems():
        key_upper = key.upper() if not context else '%s_%s' % (context, key.upper())
        if isinstance(value, dict):
            override_config(key_upper, value, new_config)
        else:
            value = override_env(key_upper) or value
            print '%s : %s' % (key_upper, value)
            new_config[key_upper] = value

def override_env(key):
    return os.environ.get(key)
    # if not environ_value:
    # 	sys.exit('Error: You must define %s environment variable' % key)

# config = Config()
# print config.get('PEOPLE_PEOPLE_HOST')
