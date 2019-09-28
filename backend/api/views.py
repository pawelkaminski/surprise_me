from http import HTTPStatus
from datetime import datetime

from flask_restful import Resource
from pymongo import MongoClient


class PingView(Resource):
    def get(self):
        with MongoClient('localhost') as client:
            client.server_info()
        return {'ping': 'pong'}, HTTPStatus.OK


class GetTextView(Resource):
    def get(self):
        return {}, HTTPStatus.OK


class GetOfferView(Resource):
    def get(self):
        mock_offer = {'start':datetime.now(), 'end': datetime.now(), 'where': 'Zurich', 'price': 10}
        return {'params': {}, 'offer': [mock_offer, mock_offer]}, HTTPStatus.OK
