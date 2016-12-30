import os
import sys

def get_environ(config, key, default=None):
	# check if param exists in config dict
	if key in config:
		value_config = config[key]
		if value_config:
			return value_config
	else:
		value_env = os.environ.get(key, default)
		if not value_env:
			sys.exit('Error: You must define %s environment variable' % key)
		return value_env
