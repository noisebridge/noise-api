import os,sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))
import bottle
import api
application = api.api_app
