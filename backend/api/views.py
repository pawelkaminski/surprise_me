from datetime import (
    datetime,
    timedelta
)

from http import HTTPStatus

from flask_restful import Resource
from pymongo import MongoClient

from backend.clients.sbb_client import SBBClient


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
        SBBClient().get_cheapest_by_location('Zürich HB', 'Bern', datetime.now() + timedelta(days=6),
                                             datetime.now() + timedelta(days=7))
        mock_offer = {'start': str(datetime.now()), 'end': str(datetime.now()), 'where': 'Zurich', 'price': 10}
        return {'params': {}, 'offer': [mock_offer, mock_offer]}, HTTPStatus.OK
