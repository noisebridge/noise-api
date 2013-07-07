#!/usr/bin/env python
##
# hello.py
###
"""hello.py

"""

__version__ = "0.1"
__author__ = ["Danny O'Brien <http://www.spesh.com/danny/> ", "Liz Henry <http://bookmaniac.org/> "]
__copyright__ = "Noisebridge"
__contributors__ = None
__license__ = "GPL v3"

from bottle import Bottle, run, request, template, TEMPLATE_PATH
from bottle import debug
from bottle import HTTPError
from bottle import redirect

import mimeparse

DEBUG = True
api_app = Bottle()
TEMPLATE_PATH.append(".")

import random
from datetime import datetime
import fcntl
import socket
import time
import re
import string


def chat_with_gate(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 30012
    try:
        s.connect(('localhost', port))
    except socket.error:
        return "Failed: Could not connect"
    data = message
    s.sendall(data)
    s.shutdown(1)
    s.settimeout(5)
    try:
        buf = s.recv(2048)
    except socket.timeout:
        buf = "Failed: No response"
    return buf

def say_out_loud(message):
        re.sub('[\W_]+', '', message)
        # this would be a lot easier if speechd wasn't broken
        command = "SPEAK\r\n"+message+"\r\n.\r\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('horsy.noise', 6560))
        except socket.error:
            return "Failed: Could not connect"
        s.send(command)
        s.settimeout(5)
        try:
            buf = s.recv(2048)
        except socket.timeout:
            buf = "Failed: No response"
        return buf

door_codes_path = "/usr/local/share/baron/codes.txt"
def load_door_codes():
    """
    Loads a list of valid access codes from door code texts list.  Lines
    starting with '#' are comments.  All other lines must contain numeric codes
    which grant access, one code per line.

    """
    new_codes = []
    with open(door_codes_path, "r") as f:
        for line in f:
            code = line.split("#")[0].strip().rstrip()
            if code.isdigit():
                new_codes.append(code)
        return new_codes

class DoorCodeException(HTTPError):
    pass

def add_door_code(oldcode, newcode = 0, comment =""):
    raise DoorCodeException(403, "Jake asked me to disable this.")
    oldcode = str(int(oldcode))
    if oldcode not in load_door_codes():
        raise DoorCodeException(403, "Your current doorcode doesn't work, so you cannot create a new doorcode.")
    if newcode == 0:
        newcode = random.randint(10000, 10000000)
    newcode = str(int(newcode))
    filtered_comment = ''.join([i for i in comment if i in (string.letters + string.punctuation + ' ')])
    if (filtered_comment is ""):
        raise DoorCodeException(403, "Please fill comment field with email or contact details")
    if len(newcode) < 6:
        raise DoorCodeException(403, "Preferred new doorcode is too short.")
    if len(newcode) > 50:
        raise DoorCodeException(403, "Preferred new doorcode is too long.")
    with open(door_codes_path, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write('%s # from %s, added %s # %s\n' % (newcode, oldcode, datetime.now(), filtered_comment))
        fcntl.flock(f, fcntl.LOCK_UN)
    return newcode

def open_gate():
    gate_message = chat_with_gate("OPEN!")
    return (gate_message, ('Acknowledged' in gate_message))

def is_gate_ringing():
    reply = chat_with_gate("Sup?")
    if (reply == "RING!\n"):
        return True
    else:
        return False

@api_app.route('/hello/:name')
def hello(name='World'):
    return '<b>Hello %s!</b>' %name


@api_app.post('/gate/key/<oldcode:int>')
def gate_key_create(oldcode=None):
    if 'create' in request.forms and request.forms.create:
        if 'preferred' in request.forms and request.forms.preferred:
            preferred_code = int(request.forms.preferred)
        else:
            preferred_code = 0
        if 'comment' in request.forms and request.forms.comment:
            comment = str(request.forms.comment)
        else:
            comment = ""
        newcode = add_door_code(oldcode, preferred_code, comment)
        redirect('/gate/key/%s' % (newcode))
    return {}

@api_app.post('/gate/')
def gate_open():
    status = gate_status()
    changes_to_status= {}
    if 'key' in request.forms and request.forms.key:
        codes = load_door_codes()
        if request.forms.key not in codes:
            status.update({ 'message' : "Key not found"})
            raise HTTPError(output="Key not found")

    if 'open' in request.forms and request.forms.open:
        gate_message, success = open_gate()
        changes_to_status = { 'open' : success , 'message' : gate_message }
        if not success:
            raise HTTPError(output = gate_message)
    status.update(changes_to_status)
    return status


def gate_status():
        return {'ringing': is_gate_ringing()}

@api_app.get('/gate/')
def get_gate_status():
    if (mimeparse.best_match(['application/json','text/html'], request.headers['accept']) == 'application/json'):
        return {'ringing': is_gate_ringing()}
    else:
        return template('gate', {'ringing' : is_gate_ringing() })

@api_app.route("/spaceapi/")
def spaceapi():
    return {  'api' : '0.11' 
            , 'space' : 'Noisebridge'
            , 'logo' : 'https://www.noisebridge.net/NB-logo-red-black-med.png'
            , 'icon' : 
            {   'open' : 'https://www.noisebridge.net/images/9/9b/Nb-open-100x100.png'
                , 'closed' : 'https://www.noisebridge.net/images/9/9b/Nb-open-100x100.png' }
            , 'url' : 'https://www.noisebridge.net/'
            , 'address' : '2169 Mission Street, San Francisco, CA 94110-1219, United States of America'
            , 'contact' : 
            {
                'irc' : 'irc://irc.freenode.net/#noisebridge'
                , 'twitter' : '@noisebridge'
                , 'ml' : 'noisebridge-discuss@noisebridge.net'
                , 'email' : 'secretary@noisebridge.net' }
            , "lat": 37.762376
            , "lon": -122.419217
            , 'open' : True
            , 'status' : 'open for public -- just ring the buzzer'
            , 'lastchange' : time.time() - 1222819200
            }

@api_app.post('/audio/')
def gate_say():
    status = {}
    changes_to_status = {}
    if 'say' in request.forms:
        utterance = request.forms.say
        changes_to_status['message'] = say_out_loud(utterance)
    status.update(changes_to_status)
    return status

def main(args):
    if DEBUG:
        print >>sys.stderr,  "In debug mode"
        debug(True)
    run(api_app,reloader=DEBUG,  host='0.0.0.0', port=8080)


import sys
import getopt


class Main():
    """ Encapsulates option handling. Subclass to add new options,
        add 'handle_x' method for an -x option,
        add 'handle_xlong' method for an --xlong option
        help (-h, --help) should be automatically created from module
        docstring and handler docstrings.
        test (-t, --test) will run all docstring and unittests it finds
        """
    class Usage(Exception):
        """ Use this to generate a Usage message """
        def __init__(self, msg):
            self.msg = msg

    def __init__(self):
        handlers = [i[7:] for i in dir(self) if i.startswith('handle_')]
        self.shortopts = ''.join([i for i in handlers if len(i) == 1])
        self.longopts = [i for i in handlers if (len(i) > 1)]

    def handler(self, option):
        i = 'handle_%s' % option.lstrip('-')
        if hasattr(self, i):
            return getattr(self, i)

    def default_main(self, args):
        print sys.argv[0], " called with ", args

    def handle_debug(self, v):
        global DEBUG
        DEBUG = True

    def handle_help(self, v):
        """ Shows this message """
        print sys.modules.get(__name__).__doc__
        descriptions = {}
        for i in list(self.shortopts) + self.longopts:
            d = self.handler(i).__doc__
            if d in descriptions:
                descriptions[d].append(i)
            else:
                descriptions[d] = [i]
        for d, opts in descriptions.iteritems():
            for i in opts:
                if len(i) == 1:
                    print '-%s' % i,
                else:
                    print '--%s' % i,
            print
            print d
        sys.exit(0)
    handle_h = handle_help

    def handle_test(self, v):
        """ Runs test suite for file """
        import doctest
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromModule(
                sys.modules.get(__name__))
        suite.addTest(doctest.DocTestSuite())
        runner = unittest.TextTestRunner()
        runner.run(suite)
        sys.exit(0)
    handle_t = handle_test

    def run(self, main=None, argv=None):
        """ Execute main function, having stripped out options and called the
        responsible handler functions within the class. Main defaults to
        listing the remaining arguments.
        """
        if not callable(main):
            main = self.default_main
        if argv is None:
            argv = sys.argv
        try:
            try:
                opts, args = getopt.getopt(argv[1:],
                        self.shortopts, self.longopts)
            except getopt.error, msg:
                raise self.Usage(msg)
            for o, a in opts:
                (self.handler(o))(a)
            return main(args)
        except self.Usage, err:
            print >>sys.stderr, err.msg
            self.handle_help(None)
            return 2

if __name__ == "__main__":
    sys.exit(Main().run(main) or 0)

