#!venv/bin/python
import os
import sys
sys.path.insert(1, os.path.abspath(os.curdir))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'lib'))

from backend import app

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
