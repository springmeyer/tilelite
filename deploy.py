
#!/usr/bin/env python

"""
Release Steps
-------------
 * write 'setup.py' file
 * create ~./pypirc file with pypi user:pass
 * register package with: 'python setup.py register'
 * Edit CHANGELOG.txt
 * Increment '__version__' in main script and 'version' in setup.py
 * Run `deploy.py` to create sdist, upload, and create tag
 * Commit tag
 * Update wiki
"""

import sys
import time
from subprocess import call as subcall

app = 'tilelite'
version = __import__(app).__version__

def call(cmd):
  try:
    response = subcall(cmd,shell=True)
    print
    time.sleep(1)
    if response < 0:
      sys.exit(response)
  except OSError, E:
    sys.exit(E)

def cleanup():
    call('sudo rm -rf *.egg* *.pyc dist/ build/')

def tag():
    call('hg tag -u springmeyer -m "tagging the %s release" %s ' % (version,version))

def upload():
    call('python setup.py sdist upload')

def main():
    cleanup()
    tag()
    upload()
    cleanup()
    
if __name__ == '__main__':
    main()