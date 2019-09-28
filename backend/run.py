from flask import Flask
from flask_restful import Api

from .api.urls import set_urls


application = Flask(__name__)
application.config.from_object('backend.settings')
api = Api(application)
config = application.config

set_urls(api, config)

# Set debug as long as it is prototype
is_debug = config.get('DEBUG', False)

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=is_debug)
