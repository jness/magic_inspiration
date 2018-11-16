#!/usr/bin/env python3

from flask import (
    Flask, render_template, request, redirect, url_for
)

from mongo import (
    find, search, random, find_one, insert_one, update_one, delete_one, distinct
)

from tools import get_sets, get_colors, get_arguments, get_ideas


# create our flask application
app = Flask(__name__)

# add a couple global template functions
app.jinja_env.globals.update(get_ideas=get_ideas)
app.jinja_env.globals.update(get_sets=get_sets)
app.jinja_env.globals.update(get_colors=get_colors)


@app.route('/', methods=['GET'])
def home():
    """
    Home page redirect to random card
    """

    return redirect(url_for('random_card'))


@app.route('/cards', methods=['GET'])
def cards():
    """
    List all cards
    """

    # keep track of our response payload
    payload = {}

    # if we recieved a POST we should add form inputs to payload
    payload.update(get_arguments(request))

    # fetch all cards matching payload
    payload['cards'] = search('cards', **payload).sort('name')

    # render our template with results
    return render_template('cards.html', **payload)


@app.route('/cards/<id>', methods=['GET'])
def card(id):
    """
    Return a card by id
    """

    # find card by id
    card = find_one('cards', _id=id)

    # if we have a result render card
    if card:
        return render_template('card.html', card=card)

    # if we do not have a result render error
    return render_template('error.html',
        message='Card id %s not found' % id), 404


@app.route('/random', methods=['GET'])
def random_card():
    """
    Get a random card
    """

    # check if we have custom filter type
    type_line = request.args.get('type_line')

    # find random card
    card = random('cards', type_line)

    # if we have a result render card
    if card:
        return redirect(url_for('card', id=card['_id']))

    # if we do not have a result render error
    return render_template('error.html',
        message='Failed to find random card'), 404


@app.route('/ideas', methods=['GET'])
def ideas():
    """
    List all ideas
    """

    # keep track of our response payload
    payload = {}

    # if we recieved a POST we should add form inputs to payload
    payload.update(get_arguments(request))

    # fetch all ideas matching payload
    payload['ideas'] = search('ideas', **payload).sort('type_line')

    # render our template with results
    return render_template('ideas.html', **payload)


@app.route('/ideas/<id>', methods=['GET'])
def idea(id):
    """
    Return a idea by id
    """

    # find idea by id
    idea = find_one('ideas', _id=id)

    # if we have a result render idea
    if idea:
        return render_template('idea.html', idea=idea)

    # if we do not have a result render error
    return render_template('error.html',
        message='Idea id %s not found' % id), 404


@app.route('/ideas/create', methods=['POST'])
def create_idea():
    """
    Create a new idea
    """

    # keep track form inputs as payload
    payload = dict(request.form.items())

    # create new object
    obj = insert_one('ideas', **payload)

    # redirect to listing page for type
    return redirect(url_for('idea', id=obj.inserted_id))


@app.route('/ideas/<id>/update', methods=['POST'])
def update_idea(id):
    """
    Update a existing idea
    """

    # keep track form inputs as payload
    payload = dict(request.form.items())

    # update object by id
    obj = update_one('ideas', id, **payload)

    # redirect to listing page for type
    return redirect(url_for('idea', id=id))


@app.route('/ideas/<id>/delete', methods=['GET'])
def delete_idea(id):
    """
    Delete an idea
    """

    # delete the document by id
    delete_one('ideas', id)

    # redirect to listing page for type
    return redirect(url_for('ideas'))


@app.route('/stories', methods=['GET'])
def stories():
    """
    List all stories
    """

    # keep track of our response payload
    payload = {}

    # if we recieved a POST we should add form inputs to payload
    payload.update(get_arguments(request))

    # fetch all cards matching payload
    payload['stories'] = search('stories', **payload).sort('name')

    # render our template with results
    return render_template('stories.html', **payload)


@app.route('/stories/<id>', methods=['GET'])
def story(id):
    """
    Return a story by id
    """

    # find story by id
    story = find_one('stories', _id=id)

    # if we have a result render story
    if idea:
        return render_template('story.html', story=story)

    # if we do not have a result render error
    return render_template('error.html',
        message='Story id %s not found' % id), 404


@app.route('/stories/create', methods=['POST'])
def create_story():
    """
    Create a new story
    """

    # keep track form inputs as payload
    payload = dict(request.form.items())

    # create new object
    obj = insert_one('stories', **payload)

    # redirect to listing page for type
    return redirect(url_for('story', id=obj.inserted_id))


@app.route('/stories/<id>/update', methods=['POST'])
def update_story(id):
    """
    Update a existing story
    """

    # keep track form inputs as payload
    payload = dict(request.form.items())

    # update object by id
    obj = update_one('stories', id, **payload)

    # redirect to listing page for type
    return redirect(url_for('story', id=id))


@app.route('/stories/<id>/delete', methods=['GET'])
def delete_story(id):
    """
    Delete an story
    """

    # delete the document by id
    delete_one('stories', id)

    # redirect to listing page for type
    return redirect(url_for('stories'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
