import json
import pymongo
from bson import ObjectId
from bson.json_util import dumps
from django.conf import settings

class LandingPage:
    def __init__(self, choice_db):
        client = pymongo.MongoClient(
            "mongodb+srv://%s:%s@production-vpq2e.mongodb.net/test?retryWrites=true&w=majority" % (
                getattr(settings, 'MONGO_CLOUD_ACCOUNT'), getattr(settings, 'MONGO_CLOUD_PASSWD')))

        self.db = client[choice_db]

    def list(self, choice_collection: str, projection: dict = None, query: dict = None) -> dict:
        if query is None:
            query = {}
        find_option = (query, projection,)
        queryset = self.db[choice_collection].find(*find_option)
        if queryset is None:
            return {'state': False, 'data': '', 'message': 'Data that does not exist.'}
        queryset = dumps(queryset)
        return {'state': True, 'data': json.loads(queryset), 'message': 'Succeed.'}

    def create(self, choice_collection: str, document: dict) -> dict:
        queryset = self.db[choice_collection].insert_one(document)
        if queryset.acknowledged:
            return {'state': True, 'data': {'inserted_id': str(queryset.inserted_id)}, 'message': 'Succeed.'}
        else:
            return {'state': False, 'data': '', 'message': 'Failed.'}

    def retrieve(self, choice_collection: str, doc_id: str, projection: dict = None) -> dict:
        if ObjectId.is_valid(doc_id):
            find_option = ({'_id': ObjectId(doc_id)}, projection,)
            queryset = self.db[choice_collection].find_one(*find_option)
            if queryset is None:
                return {'state': False, 'data': '', 'message': 'Data that does not exist.'}
            queryset = dumps(queryset)
            return {'state': True, 'data': json.loads(queryset), 'message': 'Succeed.'}
        else:
            return {'state': False, 'data': '', 'message': 'Invalid a object id.'}

    def update(self, choice_collection: str, doc_id: str, data_to_update: dict, option: dict = None) -> dict:
        if ObjectId.is_valid(doc_id):
            if option is None:
                option = {'returnNewDocument': True}
            else:
                option.update({'returnNewDocument': True})
            data_to_update.update({
                '$currentDate':
                    {
                        'lastModified': True,
                        # 'updated_date':
                        #     {
                        #         '$type': 'timestamp'
                        #     }
                    }
            })
            find_option = ({'_id': ObjectId(doc_id)}, data_to_update, option)
            queryset = self.db[choice_collection].find_one_and_update(*find_option)
            queryset = dumps(queryset)
            return {'state': True, 'data': json.loads(queryset), 'message': 'Succeed.'}
        else:
            return {'state': False, 'data': '', 'message': 'Invalid a object id.'}

    def destroy(self, choice_collection: str, doc_id: str) -> dict:
        if ObjectId.is_valid(doc_id):
            queryset = self.db[choice_collection].delete_one({'_id': ObjectId(doc_id)})
            if queryset.acknowledged:
                return {'state': True, 'data': {'deleted_id': doc_id}, 'message': 'Succeed.'}
            else:
                return {'state': False, 'data': '', 'message': 'Failed.'}
        else:
            return {'state': False, 'data': '', 'message': 'Invalid a object id.'}
