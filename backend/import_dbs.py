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

    def _import_events(self, client):
        with open('data/event.json') as event_file:
            collection = client[MONGO_DATABASE][EVENT_COLLECTION]
            collection_didok = client[MONGO_DATABASE][DIDOK_COLLECTION]
            collection.drop()
            cache = set()
            for event in json.load(event_file):
                if 'address_city' not in event:
                    continue
                if event['address_city'] in cache:
                    collection.insert_one(event)
                elif collection_didok.find_one({'Name Haltestelle': event['address_city']}):
                    collection.insert_one(event)
                    cache.add(event['address_city'])

    def _import_towns(self, client):
        with open('data/towns.csv') as towns_file:
            collection = client[MONGO_DATABASE][TOWNS_COLLECTION]
            towns = csv.DictReader(towns_file)
            for town in towns:
                collection.insert_one(town)

    def _import_didok(self, client):
        with open('data/didok.csv') as didok_file:
            collection = client[MONGO_DATABASE][DIDOK_COLLECTION]
            didoks = csv.DictReader(didok_file, delimiter=';')
            for didok in didoks:
                collection.insert_one(didok)


if __name__ == '__main__':
    DBImporter().import_db()
