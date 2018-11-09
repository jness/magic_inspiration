# **Magic Inspiration**

Magic Inspiration is a Python Flask application with a MongoDB datastore, the stack runs inside Docker with the help of docker-compose.

Using this application a game developer can come up with inspiration from [Magic the Gathering](https://magic.wizards.com) artwork, then weave an amazing story.

This application was made possible using [Scryfall](https://scryfall.com)'s bulk data files, a big thanks to them for providing an awesome data set!

![alt text](https://imgur.com/ax2LlsT.png")

## Requirements

 * [Docker](https://www.docker.com/)
 * [docker-compose](https://docs.docker.com/compose/)

## Starting Containers

Use `docker-compose` to start the stacks:

```
$ docker-compose up
```

Once complete you will be able to visit the local web interface:

 > http://localhost:5000/

## Populate Data

Once you've started the containers, use `docker-compose exec` to populate the datastore.

```
$ docker-compose exec web scripts/populate.py
```

## Purge Data

If you wish to purge the data, use `docker-compose exec` to delete documents from the datastore.
```
$ docker-compose exec web scripts/purge.py
```

## Stopping Containers

When you are done with the application use `docker-compose` to stop the containers:

```
$ docker-compose down
```
