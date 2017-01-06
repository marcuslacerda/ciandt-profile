import urllib2
import logging
import os

HOST='https://people-ciandt.appspot.com'

version = os.environ.get('TRAVIS_BUILD_NUMBER')

# [START e2e]
response = urllib2.urlopen("{}/api/public/version".format(HOST))
html = response.read()
print html
assert('0.0.%s' % version in html)
# [END e2e]
