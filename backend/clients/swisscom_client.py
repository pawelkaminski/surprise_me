from pymongo import MongoClient

from backend.settings import (
    MONGO_IP,
    MONGO_DATABASE,
    EVENT_COLLECTION,
)


class SwisscomClient:
    ACTIVITY_CATEGORIES = {
        'hiking',
        'skiing',
        'biking',
        'watersports',
        'wellness',
        'shopping',
        'panorama_trips',
        'city_trips',
        'nature_and_parks',
        'culture',
    }
    ACTIVITY_DESCRIPTIONS = {
        'hiking': 'hiking',
        'skiing': 'skiing',
        'biking': 'biking',
        'watersports': 'watersports',
        'wellness': 'wellness',
        'shopping': 'shopping',
        'panorama_trips': 'panorama_trips',
        'city_trips': 'city_trips',
        'nature_and_parks': 'nature_and_parks',
        'culture': 'culture',
    }
    ACTIVITY_SURPRISES = {
        'hiking': 'Location exploration',
        'skiing': 'Location exploration',
        'biking': 'Location exploration',
        'watersports': 'Location exploration',
        'wellness': 'Location exploration',
        'shopping': 'Location exploration',
        'panorama_trips': 'Location exploration',
        'city_trips': 'Location exploration',
        'nature_and_parks': 'Location exploration',
        'culture': 'Location exploration',
    }
    ACTIVITY_TO_CITY = {
        'hiking': ['Interlaken West', 'Glarus', 'Baden', 'Lausanne'],
        'skiing': ['Interlaken West', 'Glarus', 'Brig', 'Visp'],
        'biking': ['Interlaken West', 'Lausanne'],
        'watersports': [],
        'wellness': [],
        'shopping': [],
        'panorama_trips': [],
        'city_trips': [],
        'nature_and_parks': [],
        'culture': ['Winterthur', 'Bern', 'Aarau'],
    }

    EVENT_CATEGORIES = {
        'exhibitions',
        'sightseeing',
        'sport',
        'museums',
        'science',
        'gastronomy',
        'concerts',
        'fair_and_market'
    }

    def get_cities(self, activity, date):
        response = []
        if activity in self.ACTIVITY_CATEGORIES:
            response = self._get_activity(activity)
        elif activity in self.EVENT_CATEGORIES:
            response = self._get_event(activity, date)
        return response

    def _get_activity(self, activity):
        response = []
        response_base = {
            'surprise_name': self.ACTIVITY_SURPRISES[activity],
            'event_description': self.ACTIVITY_DESCRIPTIONS[activity],
            'event_name': activity,
            'time_start': '14:30',
            'time_end': '17:30',
            'price': 0,
        }
        for city in self.ACTIVITY_TO_CITY[activity]:
            response.append({
                'city': city,
                **response_base,
            })
        return response

    def _get_event(self, activity, date):
        responses = []
        with MongoClient(host=MONGO_IP) as client:
            collection = client[MONGO_DATABASE][EVENT_COLLECTION]
            query = {
                'date': date,
                activity: True,
            }
            response_base = {
                'surprise_name': 'Uncommon event',
                'event_description': '',
                'event_name': activity,
                'time_start': '14:30',
                'time_end': '17:30',
                'price': 0,
            }
            for event in collection.find(query):
                responses.append({
                    **response_base,
                    'event_description': event['event_description'],
                    'time_start': event['time_start'],
                    'time_end': event['time_end'],
                    'price': event['price'],
                })

                if len(responses) > 5:
                    return responses

        return responses
