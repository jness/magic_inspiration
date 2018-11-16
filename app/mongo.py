from pymongo import MongoClient
from bson.objectid import ObjectId


# create our Mongo connection
mongo = MongoClient('mongo', username='root', password='password')

# connect to collections within our database
database = mongo.magic_inspiration


def distinct(collection_name, field):
    """
    Get distinct field types
    """

    collection = getattr(database, collection_name)
    return sorted(collection.distinct(field))


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


def find_one(collection_name, **kwargs):
    """
    Perform a mongo search operation for one document
    """

    if '_id' in kwargs:
        kwargs['_id'] = ObjectId(kwargs['_id'])

    collection = getattr(database, collection_name)
    return collection.find_one(kwargs)


def find(collection_name, **kwargs):
    """
    Perform a mongo search operation
    """

    if '_id' in kwargs:
        kwargs['_id'] = ObjectId(kwargs['_id'])

    if 'color_identity' in kwargs:
        kwargs['color_identity'] = list(kwargs['color_identity'])

    collection = getattr(database, collection_name)
    return collection.find(kwargs)


def search(collection_name, **kwargs):
    """
    Perform a mongo text search against multiple fields
    """

    # fields to perform regex search against
    fields = ['name', 'type_line']

    if 'search_text' in kwargs:

        # pull search_text from kwargs
        text = kwargs['search_text']
        del(kwargs['search_text'])

        # empty mongo or query
        kwargs['$or'] = []

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


def random(collection_name, type_line=None):
    """
    Get a random document
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

    # set our sample size to 1
    filters.append({'$sample': {'size': 1}})

    collection = getattr(database, collection_name)
    document = collection.aggregate(filters)

    # return single document
    return document.next()
