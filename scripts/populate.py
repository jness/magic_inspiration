#!/usr/bin/env python3

import sys
import glob
import json
import gzip

from pymongo import MongoClient, TEXT


# create our Mongo connection
mongo = MongoClient('mongo', username='root', password='password')

# connect to collection within our database
database = mongo.magic_inspiration

# get a list of existing collections
collections = database.list_collection_names()


def populate(sets):
    """
    Populate a collection
    """

    collection_name = 'cards'

    # only populate if collection doesn't exists
    if collection_name not in collections:

        # link to our collection
        collection = getattr(database, collection_name)

        # get path to data
        path = 'data/scryfall-default-cards.json.gz'

        # open file path
        with gzip.open(path) as f:

            # load json file into python dictionary
            document = json.loads(f.read())

            # iterate over all cards
            for card in document:

                # load only our set
                if card['set'] not in sets:
                    continue

                # skip cards without flavor text
                if 'flavor_text' not in card:
                    continue

                # only want high resolution images
                if not 'highres_image':
                    continue

                # check if document already exists
                scryfall_id = card['id']

                if collection.find_one({'scryfall_id': scryfall_id}):
                    print('Document %s already exists in collection %s' % (
                        scryfall_id, collection_name)
                    )
                    continue

                # import document into collection
                print('Inserting %s into collection %s' % (
                    scryfall_id, collection_name)
                )
                collection.insert_one(card)


def main():
    """
    Main function that calls populate on all the things
    """

    populate(
        [
            'ogw', 'bfz', 'ori', 'dtk', 'frf', 'ktk', 'm15', 'jou'
            'soi', 'emn', 'kld', 'aer', 'akh', 'hou', 'xln', 'eo2',
            'rix', 'dom', 'm19', 'grn'
        ]
    )

if __name__ == '__main__':
    main()
