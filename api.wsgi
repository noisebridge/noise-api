os.chdir(os.path.dirname(__file__))
import bottle
import api
application = api.api_app()
