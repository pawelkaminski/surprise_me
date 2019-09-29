import csv
import json

from pymongo import MongoClient

from settings import (
    MONGO_IP,
    MONGO_DATABASE,
    DIDOK_COLLECTION,
    EVENT_COLLECTION,
    TOWNS_COLLECTION,
)


class DBImporter:

    def import_db(self):
        with MongoClient(host=MONGO_IP) as client:
            self._import_didok(client)
            self._import_towns(client)
            self._import_events(client)

    def _import_didok(self, client):
        with open('data/didok.csv') as didok_file:
            collection = client[MONGO_DATABASE][DIDOK_COLLECTION]
            didoks = csv.DictReader(didok_file, delimiter=';')
            for didok in didoks:
                collection.insert_one(didok)

    def _import_towns(self, client):
        with open('data/towns.csv') as towns_file:
            collection = client[MONGO_DATABASE][TOWNS_COLLECTION]
            towns = csv.DictReader(towns_file)
            for town in towns:
                collection.insert_one(town)

    def _import_events(self, client):
        event_category = self._get_event_category()
        categories = self._load_category()

        with open('data/event.json') as event_file:
            collection = client[MONGO_DATABASE][EVENT_COLLECTION]
            collection_didok = client[MONGO_DATABASE][DIDOK_COLLECTION]
            collection.drop()
            cache = set()
            for idx, event in enumerate(json.load(event_file)):
                if idx%10 == 0:
                    print(idx)
                if event['event_id'] not in event_category:
                    continue

                if event_category[event['event_id']] not in categories:
                    continue

                tag = categories[event_category[event['event_id']]]

                if 'address_city' not in event:
                    continue
                event['tag'] = tag

                if event['address_city'] in cache:
                    collection.insert_one(event)
                elif collection_didok.find_one({'Name Haltestelle': event['address_city']}):
                    collection.insert_one(event)
                    cache.add(event['address_city'])
                print(len(cache))

    def _get_event_category(self):
        result = {}
        with open('data/event_category.json') as event_category:
            for entity in json.load(event_category):
                if entity['event_id'] in result:
                    continue
                result[entity['event_id']] = entity['category_id']
        return result

    def _load_category(self):
        event_cat = {
            'exhibitions': ['Exhibitions', 'Arts', 'Other exhibitions', 'Art & design', 'Permanent exhibition',
                            'Special exhibition'],
            'sightseeing': ['Sightseeing & city tour', 'Excursion'],
            'sport': ['Sports'],
            'museums': ['History', 'Museums & Attractions', 'Other museum & attraction', 'Permanent exhibition',
                        'Special exhibition'],
            'science': ['Knowledge, computer science & environment', 'Nature / Environment', 'Cooking, Food & Taste'],
            'gastronomy': ['Culinary art', 'Special food offers', 'More Food Specials'],
            'concerts': ['Concerts others', 'Other music ads', 'Stage'],
            'fair_and_market': ['Fair & market', 'Crafts / Gold / jewelry / fashion', 'Society', 'Man / society']
        }
        reverse_map = {}
        for key, val_list in event_cat.items():
            for val in val_list:
                reverse_map[val] = key
        result = {}
        with open('data/category.json') as categories:
            for category in json.load(categories):
                if 'title_en' not in category:
                    continue
                if category['title_en'] not in reverse_map:
                    continue
                result[category['category_id']] = reverse_map[category['title_en']]
        return result


if __name__ == '__main__':
    DBImporter().import_db()
