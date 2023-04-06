# Cap'em

![GitHub](https://img.shields.io/github/license/Ananto30/cap-em)
[![Build Status](https://travis-ci.com/Ananto30/cap-em.svg?branch=master)](https://travis-ci.com/Ananto30/cap-em)
[![codecov](https://codecov.io/gh/Ananto30/cap-em/branch/master/graph/badge.svg)](https://codecov.io/gh/Ananto30/cap-em)
![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/ananto30/cap-em?logo=docker)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/Ananto30/cap-em.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Ananto30/cap-em/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Ananto30/cap-em.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Ananto30/cap-em/context:python)
[![Maintainability](https://api.codeclimate.com/v1/badges/620b4efcf9e41d74cb00/maintainability)](https://codeclimate.com/github/Ananto30/cap-em/maintainability)
[![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/Ananto30/cap-em?logo=Code%20Climate)](https://codeclimate.com/github/Ananto30/cap-em/trends/technical_debt)

The next generation limit tracker! If you are working in a fast growing company (it doesn't matter) you might have faced a situation where you need rate limit your api with several configurations. In that case rather rate limiting your API you can use Cap'em as a service to track your resource usage with limiters. You can deploy this as an independent service ([Docker-ready](https://hub.docker.com/r/ananto30/cap-em)).

## Feature & Principle

Say you have a resource called Email. You want to limit this email change capacity for users. This is set to twice per day. You are very happy to code with that, now the requirements come again and said twice per day but not more than one per hour, and monthly limit should be 5 🤬Now Cap-em will come to the rescue! It's an independent service, so you can deploy in your microservices or SOA.

You can have different configurations like above or as many configs as you like with several resources. All you need is to make a config file, and use the service right away! Please refer to [Usage](#Usage) for details.

## Installation-Dev

There's several way to install and run.

First, let's see the typical way, using Python (3.7.3 preffered). 
```bash
pip install -r requirements.txt
sh start_server.sh
# create table manually, or by this command
python -m app.create_table
```
How intuitive! 😅The local server will by default use a SQLite `'sqlite:///capem.db'`, you can find this in the `db/base.py` file. If you want to use the Postgres from the docker-compose - 
```bash
docker-compose up -d
DB_URI=postgres://capem:pass@localhost:5432/postgres sh start_server.sh
```
Change the `DB_URI` as per your relational DB uri.

IMPORTANT!!: Please note that in this case, we are using Gunicorn and we are copying our config file from source directory to app directory, so please remove that file after playing locally, specially before building a docker image, the docker image has a shared volume to work with the file.

Second, you can just use Docker! 😁 Make sure you have changed the `DB_URI` environment variable in the `start_docker.sh` file. [Here](#docker) is the detailed Docker example.
```bash
docker-compose up -d
sh build_docker.sh
sh start_docker.sh
```

It will start running in http://localhost:8003

## Usage

For now only the REST API's are available to use.

First we need to make the config file. An example can be found in the `config/config.txt`. All you need is to edit this file.

Configurations are like this - 
```
email,60:2,3600:5,86400:6
```
What does it mean? The first one, `email` is the resource. Then `60:2` means in 60 seconds the limit is 2 to change/access the resource. The rest are configs for different time intervals and limits. Please follow the format as it is. The **time increases in ascending order**. And `60:5,3600:2` doesn't make sense, yet it will work. 

Like the problemd mentioned [above](#feature--principle). The configuration will be - 
```
email,3600:1,86400:2,2592000:5
```
So add configurations like this, new configs in new lines. Please note that everything is in **SECONDS**.

### API

Now let's come to the API usage. For checking the limit use this - 
```bash
curl --location --request POST 'localhost:8003/limit/check' \
--header 'Content-Type: application/json' \
--data-raw '{
	"resource_name": "email",
	"access_id": "ananto"
}'
```
This returns `has_limit` which is boolean, and `access_in` which is int. `access_in` returns 0 if `has_limit` is true, otherwise returns how many seconds left to use that resource again.

To increase usage, use this - 
```bash
curl --location --request POST 'localhost:8003/add/usage' \
--header 'Content-Type: application/json' \
--data-raw '{
	"resource_name": "email",
	"access_id": "ananto"
}'
```
After successful `/limit/check` you may `/add/usage`. But be cautious that you don't `/add/usage` without serving your user. The case can be like this - user "dd45bi6" wants to edit the email, you check the limit with `/limit/check`, if they get `has_limit` true, let them edit the email, after successful email change, you increase the resource usage by `/add/usage`.


You can also see the configs -
```bash
curl --location --request GET 'localhost:8003/config'
```

## Docker

### Local/Dev

If you want to run it locally, just clone the repo and build the image -
```bash
git clone https://github.com/Ananto30/cap-em.git
cd cap-em
docker-compose up -d  # if you want to use the docker postgres
docker build -t capem/flask . 
```

Then just start with the shell file if you want to use the docker postgres (you may want to change the environment variable `DB_URI` with your ip)
```bash
sh start_docker.sh
```
OR run with this command 
```bash
docker run --name capem -v $(pwd)/config:/app/config -p 8003:8003 -e DB_URI=your_db_uri capem/flask
```
Make sure the config file is the proper directory. Should be in `/config`.

You can change base service port from `gunicorn_starter.sh` file. *Also for production you can tweak with workers and threads.*

### Production

This is the much preferred way to use the service out of the box. And kind of production ready. You don't need to clone the repo, you can pull the image from docker hub.
```bash
docker pull ananto30/cap-em
```
You need to add the config directory `./config` and put the `confgi.txt` file there (`./config/config.txt`). Then run with this command - 
```bash
docker run --name capem -v $(pwd)/config:/app/config -p 8003:8003 -e DB_URI=your_db_uri ananto30/cap-em
```
Make sure to properly configure `-v $(pwd)/config:/app/config` and `-e DB_URI=your_db_uri` for your production.

This config volume is under your control. You can choose to use an existing volume of your own, or create a new one, or use like above (create in the directory from where you want to run the image).


## Tests

Tests are better to be run with SQLite database. Because there will be entries in DB and those should be cleared after each test is run. So **if you use any other than sqlite, make sure to delete the entries to pass tests**. To use SQLite you need to set the environment variable `DB_URI` -
```bash
DB_URI=sqlite:///capem-ut.db python -m pytest 
```

To run tests with coverage - 
```bash
DB_URI=sqlite:///capem-ut.db python -m pytest --cov=./app
```

## Local Development

There's several way to run locally for development (though this an independent and complete service, encouraged to use out of the box, but you may modify on your own).

You can follow the [Installation-Dev](#installation-dev) to run locally, but for solely development purpose you can run like this - 

```bash
pip install -r requirements.txt
python -m app.create_table # create table manually, or by this command
python -m app.main
```
This uses the SQLite DB, to change that, use `DB_URI` env variable.


## Production [Half ready]

Need to optimize Docker and indexing DB (not sure).

But still you can use in production out of the box. Preferred way is to use the [Docker production](#production).


## TODO
Priority
- A persistant way for configs? Like redis, so that multiple workers can get the same config
- Generalize the volume thing, this is somewhat a dependency
- Local caching is good but how to share the configs with different workers when config get changed
- Endpoint(s) to up new configs, in bulk or single

Less priority
- A docker-compose for whole project up in local
- Add more tests
- gRPC?
- Messaging (for event-driven services)
- Non-relational DB support?
