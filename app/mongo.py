from pymongo import MongoClient
from bson.objectid import ObjectId


# create our Mongo connection
mongo = MongoClient('mongo', username='root', password='password')

# connect to collections within our database
database = mongo.magic_inspiration


def insert_one(collection_name, **kwargs):
    """
    Insert document into mongo
    """

    collection = getattr(database, collection_name)
    return collection.insert_one(kwargs)


def update_one(collection_name, _id, **kwargs):
    """
    Update document in mongo
    """

    collection = getattr(database, collection_name)
    return collection.update_one({'_id': ObjectId(_id)}, {'$set': kwargs})


def delete_one(collection_name, _id):
    """
    Delete document into mongo
    """

    collection = getattr(database, collection_name)
    return collection.delete_one({'_id': ObjectId(_id)})


def find(collection_name, **kwargs):
    """
    Perform a mongo search operation
    """

    if '_id' in kwargs:
        kwargs['_id'] = ObjectId(kwargs['_id'])

    collection = getattr(database, collection_name)
    return collection.find(kwargs)


def full_text(collection_name, text):
    """
    Perform a mongo full text search
    """

    # fields to perform regex search against
    fields = ['name', 'type_line']

    # empty mongo or query
    kwargs = {'$or': []}

    # populate mongo or query with all fields
    for field in fields:
        kwargs['$or'].append(
            {
                field: {
                    '$regex': text,
                    '$options': 'i'
                }
            }
        )

    return find(collection_name, **kwargs)


def find_one(collection_name, **kwargs):
    """
    Perform a mongo search operation for one document
    """

    if '_id' in kwargs:
        kwargs['_id'] = ObjectId(kwargs['_id'])

    collection = getattr(database, collection_name)
    return collection.find_one(kwargs)


def find_cards(**kwargs):
    """
    Get all cards with optional keyword arguments
    """

    return find('cards', **kwargs).sort('name')


def find_random_card(type_line=None):
    """
    Find a random card
    """

    # empty list for filters
    filters = []

    # match against type_line if asked
    if type_line:
        filters.append(
            {
                '$match': {
                    'type_line': {
                        '$regex': type_line,
                        '$options': 'i'
                    }
                }
            }
        )

    # get a single random card
    filters.append({'$sample': {'size': 1}})

    collection = getattr(database, 'cards')
    cards = collection.aggregate(filters)

    # get our single card
    return cards.next()
