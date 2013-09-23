#!/usr/bin/env python

import os
import sys
import socket
import logging
from optparse import OptionParser
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler

CONFIG = 'tilelite.cfg'
MAP_FROM_ENV = 'MAPNIK_MAP_FILE'
    
parser = OptionParser(usage="""
    python liteserv.py <mapfile.xml> [options]
    """)

parser.add_option('-i', '--ip', default='0.0.0.0', dest='host',
    help='Specify a ip to listen on (defaults to 0.0.0.0/localhost)'
    )

parser.add_option('-p', '--port', default=8000, dest='port', type='int',
    help='Specify a custom port to run on: eg. 8080'
    )

parser.add_option('--config', default=None, dest='config',
    help='''Specify the use of a custom TileLite config file to override default settings. By default looks for a file locally called 'tilelite.cfg'.'''
    )

parser.add_option('-s', '--size', default=None, dest='size', type='int',
    help='Specify a custom tile size (defaults to 256)'
    )

parser.add_option('-b', '--buffer-size', default=None, dest='buffer_size', type='int',
    help='Specify a custom map buffer_size (defaults to 128)'
    )

parser.add_option('-z', '--max-zoom', default=None, dest='max_zoom', type='int',
    help='Max zoom level to support (defaults to 22)'
    )
    
parser.add_option('-f', '--format', default=None, dest='format',
    help='Specify a custom image format (png or jpeg) (defaults to png)'
    )

parser.add_option('--paletted', default=False, dest='paletted', action='store_true',
    help='Use paletted/8bit PNG (defaults to False)'
    )

parser.add_option('-d','--debug', default=True, dest='debug', type="choice", choices=('True','False'),
    help='Run in debug mode (defaults to True)'
    )

parser.add_option('-c','--caching', default=False, dest='caching', action='store_true',
    help='Turn on tile caching mode (defaults to False)'
    )

parser.add_option('--cache-path', default=None, dest='cache_path',
    help='Path to tile cache directory (defaults to "/tmp")'
    )

parser.add_option('--cache-force', default=False, dest='cache_force', action='store_true',
    help='Force regeneration of tiles while in caching mode (defaults to False)'
    )

parser.add_option('--processes', default=1, dest='num_processes', type='int',
    help='If werkzeug is installed, number of rendering processes to allow'
    )

parser.add_option('--threaded', default=False, dest='threaded', action='store_true',
    help='If werkzeug is installed, place each request on a new thread'
    )
    
def run(process):
    try:
        process.serve_forever()
    except KeyboardInterrupt:
        process.server_close()
        sys.exit(0)

def strip_opts(options):
    remove = [None,'config','port','host']
    params = {}
    for k,v in options.items():
        if not k in remove and not v is None:
            params[k] = v
    return params

def print_url(options):
    if not application.debug:
        sys.stderr.write('TileLite debug mode is *off*...\n')
    sys.stderr.write("Listening on %s:%s...\n" % (options.host,options.port))
    sys.stderr.write("To access locally view: http://localhost:%s\n" % options.port)
    remote = "To access remotely view: http://%s" % socket.getfqdn()
    if not options.port == 80:
        remote += ":%s" % options.port
    try:
        remote += "\nor view: http://%s" % socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        pass
    if not options.port == 80:
        remote += ":%s" % options.port
    sys.stderr.write('%s\n' % remote)

if __name__ == '__main__':
    (options, args) = parser.parse_args()
    log = logging.getLogger('tilelite.liteserv')
        
    if len(args) < 1:
        try:
            mapfile = os.environ[MAP_FROM_ENV]
        except:
            sys.exit("\nPlease provide either the path to a mapnik xml or\nset an environment setting called '%s'\n" % (MAP_FROM_ENV))
    else:
        mapfile = args[0]
        if not os.path.exists(mapfile):
            sys.exit('Could not locate mapfile.')
    
    logging.basicConfig(level=(logging.DEBUG if options.debug else logging.INFO))
    log.debug("Using mapfile: '%s'", os.path.abspath(mapfile))
        
    if options.config:
        if not os.path.isfile(options.config):
            sys.exit('That does not appear to be a valid config file')
        else:
            CONFIG = options.config

    if not os.path.exists(CONFIG):
        if options.config:
            sys.exit('Could not locate custom config file')
        else:
            CONFIG = None
    
    if CONFIG:
        log.debug("Using config file: '%s'", os.path.abspath(CONFIG))

    if options.cache_path and not options.caching:
        options.caching = True

    if options.cache_force and not options.caching:
        options.caching = True

    #parser.error("Caching must be turned on with '--caching' flag for liteserv.py to accept '--cache-path' option")
    #http_setup = options.host, options.port
    #httpd = simple_server.WSGIServer(http_setup, WSGIRequestHandler)
    #httpd.set_app(application)

    from tilelite import Server
    application = Server(mapfile, CONFIG)
    application.absorb_options(strip_opts(options.__dict__))
                
    try:
        from werkzeug import run_simple
        print_url(options)
        run_simple(options.host, options.port, application, threaded=options.threaded, processes=options.num_processes)
    except:
        if options.num_processes > 1:
            sys.exit('The werkzeug python server must be installed to run multi-process\n')
        sys.stderr.write('Note: werkzeug is not installed so falling back to built-in python wsgiref server.\n')
        sys.stderr.write('Install werkzeug from http://werkzeug.pocoo.org/\n\n')
        
        from wsgiref import simple_server
        # below code was for testing multi-threaded rendering
        # which only works if we copy a map object per thread
        # so avoid this and only run multiprocess...
        #from SocketServer import ThreadingMixIn
        #class myServer(ThreadingMixIn, simple_server.WSGIServer):
        #    pass 
        #httpd = myServer(('',options.port), simple_server.WSGIRequestHandler,)
        #httpd.set_app(application)
        httpd = make_server(options.host, options.port, application)        
        print_url(options)
        run(httpd)
        
