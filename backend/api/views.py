from datetime import (
    datetime,
    timedelta
)

from http import HTTPStatus

from flask import request
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
    def post(self):
        """
        Expected data:
        {
            "activity": "String",
            "departure_location": "String",
            "schedule": "Date",
            "maxPrice": "Number",
            "participants": "Number"
        }

        {
            "departure_schedule": "DateT",
            "departure_location": "String",
            "arrival_schedule": "Date",
            "arrival_location": "String",
            "price": "String",
            "participants": "Number",
            "suprise_name":"String",
            "event_name": "String",
            "event_description":"String"
        }
        :return:
        """
        request_json = request.get_json()
        print(request_json['maxPrice'])
        print(request_json['activity'])
        print(request_json['schedule'])

        # SBBClient().get_cheapest_by_location('Zürich HB', 'Bern', datetime.now() + timedelta(days=6),
        #                                      datetime.now() + timedelta(days=7))
        mock_offer = {
            'departure_schedule': '2019-09-29T15:30',
            'arrival_schedule': '2019-09-29T19:35',
            'departure_location': request_json['departure_location'],
            'arrival_location': 'Bern',
            'price': 120,
            'participants': request_json['participants'],
            'suprise_name': 'Nobody expects Spanish inquisition',
            'event_name': 'Hiking concert',
            'event_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        }

        return mock_offer, HTTPStatus.OK
