from mongo import (
    find, search, random, find_one, insert_one, update_one, delete_one, distinct
)


def get_ideas():
    """
    Gets all ideas from mongo
    """

    return find('ideas')


def get_sets():
    """
    Gets all distinct sets from mongo
    """

    return distinct('cards', 'set_name')


def get_colors():
    """
    Get all distinct color_identity from mongo
    """

    return sorted(
        set(
            [''.join(i['color_identity']) for i in find('cards')]
        )
    )


def get_arguments(request):
    """
    Return request arguments as dict
    """

    return {key:value for key, value in request.args.items() if value}
