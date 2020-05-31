# Cap-em

The next generation limit tracker! If you are working in a fast growing company (it doesn't matter) you might have faced a product manager with unrealistic configurations 😐This service will help you somehow in that case 😅

Main purpose is to rate-limit or track usage limit of your resources in every configuration possible. Please refer to [Usage](#Usage) for details.

## Feature & Principle

Say you have a resource called Email. You (mostly your product manager) want to limit this email change capacity for users. This is set to twice per day. You are very happy to code with that, now the PM comes again and said twice per day but not more than one per hour, and monthly limit should be 5 🤬 Now Cap-em will come to the rescue! It's an independent service, so you can deploy in your microservices or SOA.

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
How intuitive! 😅 The local server will by default use a SQLite `'sqlite:///capem.db'`, you can find this in the `db/base.py` file. If you want to use the Postgres from the docker-compose - 
```bash
docker-compose up -d
DB_URL=postgres://capem:pass@localhost:5432/postgres sh start_server.sh
```
Change the `DB_URL` as per your relational DB uri.

IMPORTANT!!: Please note that in this case, we are using Gunicorn and we are copying our config file from source directory to app directory, so please remove that file after playing locally, specially before building a docker image, the docker image has a shared volume to work with the file.

Second, you can just use Docker! 😁 Make sure you have changed the `db_url` arg in the `build_docker.sh` file (if you are not using the docker-compose postgres). [Here](#docker-out-of-the-box-deployment) is the detailed Docker example.
```bash
docker-compose up -d
sh build_docker.sh
sh start_docker.sh
```

It will start running in http://localhost:8003

## Usage

For now only the REST API's are available to use.

First we will learn to make the config file. An example can be found in the `config/config.txt`. All you need is to edit this file.

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


## Docker [Out of the box deployment]

This is the much preferred way to use the service out of the box. And kind of production ready. Just make sure to change the `ARG db_url` in `Dockerfile` to your expected DB, then run -
```bash
docker build -t capem/flask . 
```
OR run with build argument, no need to change the `ARG db_url` in this case
```bash
docker build --build-arg db_url=postgres://capem:pass@192.168.0.107:5432/postgres -t capem/flask . 
```

Then just start with the shell file
```bash
sh start_docker.sh
```
OR run with this command 
```bash
#!/bin/bash
docker run --name capem -v $(pwd)/config:/app/config -p 8003:8003 capem/flask
```
Make sure the config file is the proper directory. Should be in `/config`.


You can change port from `gunicorn_starter.sh` file. *Also for production you can tweak with workers and threads.*

## Tests

Tests are better to be run with SQLite database. Because there will be entries in DB and those should be cleared after each test is run. So **if you use any other than sqlite, make sure to delete the entries to pass tests**. To use SQLite you need to set the environment variable `DB_URL` -
```bash
DB_URL=sqlite:///capem-ut.db python -m pytest 
```

To run tests with coverage - 
```bash
DB_URL=sqlite:///capem-ut.db python -m pytest --cov=./app
```

## Development [Locally]

There's several way to run locally for development (though this an independent and complete service, encouraged to use out of the box, but you may modify on your own).

You can follow the [Installation-Dev](#installation-dev) to run locally, but for solely development purpose you can run like this - 

```bash
pip install -r requirements.txt
python -m app.create_table # create table manually, or by this command
python -m app.main
```
This uses the SQLite DB, to change that, use `DB_URL` env variable.


## Production [Half ready]

Need to optimize Docker and indexing DB (not sure).

But still you can use in production out of the box. Preferred way is to use the [Docker](#docker-out-of-the-box-deployment).


## TODO
- Add more tests
- gRPC?
- Messaging (for event-driven services)
