#! /usr/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/html/')
from app import app as application
application.secret_key = '0Ncs92894fhno'
