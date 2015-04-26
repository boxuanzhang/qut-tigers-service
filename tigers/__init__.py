
__all__ = [
    'app'
]

#
# Build basic Flask app
#

# Import flask
from flask import Flask

# Build WSGI application
app = Flask(__name__)

# Load configurations
app.config.from_object('config')

#
# Build mongodb connection
#

# Connect database
from mongoengine import connect

connect(
    app.config['MONGODB_DB'],
    host=app.config['MONGODB_HOST'],
    port=app.config['MONGODB_PORT'],
)


#
# Build RESTful service
#
from flask.ext.restful import Api

api = Api(app)

# Auth
from tigers.resources.auth import Auth
api.add_resource(Auth, '/auth')

# Status
from tigers.resources.status import Status, StatusList
api.add_resource(StatusList, '/status')
api.add_resource(Status, '/status/<status_id>')

# Photo
from tigers.resources.photo import Photo, PhotoToken
api.add_resource(Photo, '/photo/<photo_id>')
api.add_resource(PhotoToken, '/photo_token')
