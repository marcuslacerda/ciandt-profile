"""Package for tests."""
import os
import sys

sys.path.insert(1, os.path.abspath(os.curdir))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'lib_tests'))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'jobs'))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'server', 'app'))

# print sys.path
