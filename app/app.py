#!/usr/bin/env python3

import re

# 3rd party modules
from flask import (
    Flask, render_template, request, redirect, url_for
)

from mongo import (
    find, find_cards, find_one, full_text, find_random_card, insert_one,
    update_one, delete_one
)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def cards():
    """
    List all cards
    """

    # get all cards
    cards = find_cards()

    # render our template with results
    return render_template('cards.html', cards=cards)


@app.route('/card_search', methods=['GET'])
def card_search():
    """
    List filtered card
    """

    # required url params for search
    search_text = request.args.get('search_text')

    # perform search against all fields
    cards = full_text('cards', search_text)

    # # render our template with results
    return render_template(
        'cards.html',
        search_text=search_text,
        cards=cards
    )


@app.route('/card/<id>', methods=['GET'])
def card(id):
    """
    Return a card by name
    """

    # find card by id
    card = find_one('cards', _id=id)

    # if we have a result render card
    if card:
        return render_template('card.html', card=card)

    # if we do not have a result render error
    return render_template('error.html',
        message='Card %s not found' % id), 404


@app.route('/random', methods=['GET'])
def random():
    """
    Get a random card
    """

    # check if we have custom filter type
    type_line = request.args.get('type_line')

    # find random card
    card = find_random_card(type_line)

    # if we have a result render card
    if card:
        return redirect(url_for('card', id=card['_id']))

    # if we do not have a result render error
    return render_template('error.html',
        message='Failed to find random card'), 404


@app.route('/create', methods=['POST'])
def create():
    """
    Create a new idea
    """

    # grab required form elements from POST
    name = request.form['name']
    type_line = request.form['type_line']
    flavor_text = request.form['flavor_text']
    art_crop = request.form['art_crop']
    artist = request.form['artist']
    notes = request.form['notes']

    obj = insert_one('ideas', name=name, type_line=type_line,
        flavor_text=flavor_text, art_crop=art_crop, artist=artist,
        notes=notes)

    return redirect(url_for('idea', id=obj.inserted_id))


@app.route('/update', methods=['POST'])
def update():
    """
    Update a existing idea
    """

    # grab required form elements from POST
    id = request.form['id']
    name = request.form['name']
    type_line = request.form['type_line']
    flavor_text = request.form['flavor_text']
    notes = request.form['notes']

    obj = update_one('ideas', id, name=name, type_line=type_line,
        flavor_text=flavor_text, notes=notes)

    return redirect(url_for('idea', id=id))


@app.route('/delete', methods=['GET'])
def delete():
    """
    Delete an idea
    """

    # check if we have custom filter type
    id = request.args.get('id')

    # delete the document by id
    delete_one('ideas', id)

    # redirect to ideas page
    return redirect(url_for('ideas'))


@app.route('/ideas', methods=['GET'])
def ideas():
    """
    List all ideas
    """

    # get all ideas
    ideas = find('ideas')

    # render our template with results
    return render_template('ideas.html', ideas=ideas)


@app.route('/idea_search', methods=['GET'])
def idea_search():
    """
    List filtered ideas
    """

    # required url params for search
    search_text = request.args.get('search_text')

    # perform search against all fields
    ideas = full_text('ideas', search_text).sort('type')

    # # render our template with results
    return render_template(
        'ideas.html',
        search_text=search_text,
        ideas=ideas
    )


@app.route('/idea/<id>', methods=['GET'])
def idea(id):
    """
    Return a idea by id
    """

    # find idea by id
    idea = find_one('ideas', _id=id)

    # if we have a result render card
    if idea and card:
        return render_template('idea.html', idea=idea)

    # if we do not have a result render error
    return render_template('error.html',
        message='Idea %s not found' % id), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
