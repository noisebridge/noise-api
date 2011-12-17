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

from bottle import Bottle, run
from bottle import debug

DEBUG = False
api_app = Bottle()

import socket

def chat_with_gate(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 30012
    try:
        s.connect(('minotaur.noise', port))
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

def open_gate():
    return chat_with_gate("OPEN!")

def is_gate_ringing():
    reply = chat_with_gate("Sup?")
    if (reply == "RING!\n"):
        return True
    else:
        return False

@api_app.route('/hello/:name')
def hello(name='World'):
    return '<b>Hello %s!</b>' %name


@api_app.post('/gate/open')
def gate_open():
    gate_message = open_gate()
    return { 'success' : ('Acknowledged' in gate_message), 'message' : gate_message }

@api_app.get('/gate/')
def gate_status():
    return { 'ringing' : is_gate_ringing() }


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

