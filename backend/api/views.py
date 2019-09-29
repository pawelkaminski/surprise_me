from datetime import (
    datetime,
    timedelta
)

from http import HTTPStatus

from flask import request
from flask_restful import Resource
from pymongo import MongoClient

from backend.clients.sbb_client import SBBClient
from backend.clients.swisscom_client import SwisscomClient


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
            "max_price": "Number",
            "participants": "Number"
        }
        {
            "departure_schedule": "DateT",
            "departure_location": "String",
            "arrival_schedule": "Date",
            "arrival_location": "String",
            "price": "String",
            "participants": "Number",
            "surprise_name":"String",
            "event_name": "String",
            "event_description":"String"
        }
        :return:
        """
        request_json = request.get_json()
        request_json['departure_location'] = 'Zürich HB'

        if request_json['activity'] in ('hiking', 'rock concert'):
            return self._process_cache(request_json), HTTPStatus.OK

        activity_cities = self._get_cities_with_timeframes(request_json['activity'], request_json['schedule'])
        result = self._get_cheapest_sbb_tickets(activity_cities, request_json['departure_location'],
                                                request_json['schedule'])

        # TODO(pawelk): if keyword run cached offer
        # mock_offer = self._get_from_cache(request_json)

        print(result)

        if not result:
            result = self._get_from_cache(request_json)

        result.update({
            'participants': request_json['participants'],
            'departure_location': request_json['departure_location'],
        })

        return result, HTTPStatus.OK

    def _get_cities_with_timeframes(self, activity, date):
        cities = SwisscomClient().get_cities(activity, date)
        print(cities)
        return cities
        # return [{
        #     'surprise_name': 'Location exploration',
        #     'event_name': 'Hiking concert',
        #     'event_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        #     'city': 'Bern',
        #     'time_start': '15:30',
        #     'time_end': '17:30',
        #     'price': 0,
        # }, {
        #     'surprise_name': 'Uncommon event',
        #     'event_name': 'Hiking concert',
        #     'event_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        #     'city': 'Luzern',
        #     'time_start': '15:30',
        #     'time_end': '17:30',
        #     'price': 0,
        # }]

    def _get_cheapest_sbb_tickets(self, activities, start_location, date):
        client = SBBClient()
        results = []
        for activity in activities:
            cheapest_trip = client.get_cheapest_by_location(
                start_location,
                activity['city'],
                self._datetime_from_string(date+'T'+activity['time_start']) - timedelta(hours=6),
                self._datetime_from_string(date+'T'+activity['time_end'])
            )
            cheapest_trip['arrival_location'] = activity['city']
            for key in ('event_name', 'event_description', 'surprise_name'):
                cheapest_trip[key] = activity[key]
            cheapest_trip['price'] += activity['price']
            results.append(cheapest_trip)

        min_price = 10**8
        top_result = None
        for result in results:
            if result['price'] < min_price:
                top_result = result
                min_price = top_result['price']
        return top_result

    def _datetime_from_string(self, string):
        return datetime.strptime(string, '%Y-%m-%dT%H:%M')

    def _get_from_cache(self, request_json):
        return {
            'departure_schedule': '2019-09-29T15:30',
            'arrival_schedule': '2019-09-29T19:35',
            'departure_location': request_json['departure_location'],
            'arrival_location': 'Bern',
            'price': 120,
            'participants': request_json['participants'],
            'surprise_name': 'Nobody expects Spanish inquisition',
            'event_name': 'Hiking concert',
            'event_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        }

    def _process_cache(self, request_json):
        if request_json['activity'] == 'hiking':
            return {
                'departure_schedule': request_json['schedule']+'T08:20',
                'arrival_schedule': request_json['schedule']+'T18:37',
                'departure_location': request_json['departure_location'],
                'arrival_location': 'Flumserberg',
                'price': 2900,
                'participants': request_json['participants'],
                'surprise_name': 'Wanderungen im Heidiland.',
                'event_name': 'Hiking: Flumserberg',
                'event_description': 'From Tannenboden you reach the beautiful surroundings of Seeben on the hiking trail via Winkelzahn. The hike around the Seebensee lake with the Churfirsten mountains behind invites you to marvel. After these beautiful impressions you return to Winkelzahn. The beautiful hiking route leads through the forest to the mountain station, then follow the path to Chrüz.',
            }
        else:
            return {
                'departure_schedule': request_json['schedule']+'T15:11',
                'arrival_schedule': request_json['schedule']+'T21:23',
                'departure_location': request_json['departure_location'],
                'arrival_location': 'Baden',
                'price': 7600,
                'participants': request_json['participants'],
                'surprise_name': 'Bell Baronets & Elio Ricca @ Royal Baden',
                'event_name': 'Bell Baronets & Elio Ricca @ Royal Baden',
                'event_description': 'Loud, raw and with distortion in the blood. The Bell Baronets are back; with a new album and, as they say, ready to climb the rock sky. They combine their 70s vibe skillfully but unconventionally with contemporary musical influences resulting in an explosive jam. Their diverse stage experience and a sustained maturation process give free rein to our anticipation.',
            }


