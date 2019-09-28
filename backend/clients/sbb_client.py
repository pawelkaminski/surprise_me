from pymongo import MongoClient
import requests

from backend.settings import (
    MONGO_IP,
    MONGO_DATABASE,
    DIDOK_COLLECTION,
)


class SBBClient:

    BASE_SBB_URL = 'https://sso-int.sbb.ch/'
    BASE_SBB_APP_URL = 'https://b2p-int.api.sbb.ch'

    def get_cheapest_by_location(self, location_from, location_to, from_date, to_date):
        token = self._get_token()
        city_from_id = self._get_city_id(location_from)
        city_to_id = self._get_city_id(location_to)

        headers = {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'X-Contract-Id': 'ABC1234',
            'X-Conversation-Id': 'e5eeb775-1e0e-4f89-923d-afa780ef844b',
            'Accept-Language': 'en',
        }

        tickets_to = self._get_trips(from_date, city_from_id, city_to_id, headers)
        tickets_from = self._get_trips(to_date, city_to_id, city_from_id, headers)

    def _get_token(self):
        response = requests.post(self.BASE_SBB_URL+'/auth/realms/SBB_Public/protocol/openid-connect/token', {
            'grant_type': 'client_credentials',
            'client_id': '22ebc2be',
            'client_secret': '2c820784f3e28837959abc43120989ca',
            'contract_id': 'HAC222P',
        })
        return response.json()['access_token']

    def _get_city_id(self, city_name):
        with MongoClient(host=MONGO_IP) as client:
            collection = client[MONGO_DATABASE][DIDOK_COLLECTION]
            return collection.find_one({'Name Haltestelle': city_name})['didok85']

    def _get_trips(self, start_time, city_from_id, city_to_id, headers):
        params = {
            'date': str(start_time.date()),
            'time': str(start_time.time())[:5],
            'destinationId': city_to_id,
            'originId': city_from_id,
            'passengers': 'paxa;42;half-fare',
        }

        response = requests.get(self.BASE_SBB_APP_URL + '/api/trips', params=params, headers=headers)
        obtained_trips = []
        for el in response.json():
            obtained_trips.append({
                'tripId': el['tripId'],
                'arrivalDateTime': el['segments'][0]['destination']['arrivalDateTime'],
                'departureDateTime': el['segments'][0]['origin']['departureDateTime'],
                'price': self._get_price(el['tripId'], headers['Authorization'])
            })
        return obtained_trips

    def _get_price(self, trip_id, auth):
        params = {
            'qualityOfService': 2,
            'tripIds': [trip_id],
            'passengers': 'paxa;42;half-fare',
        }

        headers = {
            'Authorization': auth,
            'Accept': 'application/json',
            'X-Contract-Id': 'ACP1024',
            'X-Conversation-Id': 'cafebabe-0815-4711-1234-ffffdeadbeef',
            'Accept-Language': 'en',
        }
        response = requests.get(self.BASE_SBB_APP_URL + '/api/v2/prices', params=params, headers=headers)
        return response.json()[0]['price']
