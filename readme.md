# Cap'em

[![GitHub](https://img.shields.io/github/license/Ananto30/cap-em)](/LICENSE.md)
[![codecov](https://codecov.io/gh/Ananto30/cap-em/branch/main/graph/badge.svg)](https://codecov.io/gh/Ananto30/cap-em)
[![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/ananto30/cap-em?logo=docker)](https://hub.docker.com/r/ananto30/cap-em)

[![Maintainability](https://api.codeclimate.com/v1/badges/620b4efcf9e41d74cb00/maintainability)](https://codeclimate.com/github/Ananto30/cap-em/maintainability)
[![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/Ananto30/cap-em?logo=Code%20Climate)](https://codeclimate.com/github/Ananto30/cap-em/trends/technical_debt)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9bbb9f74a480493f9891e9ea015e4eb0)](https://app.codacy.com/gh/Ananto30/cap-em/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

Easy to use **resource usage tracker** (can be used as a rate limiter). Define a config file and use it right away! Use the **production ready** [Docker](#run-it-now-🚀) image or run it locally.

## Usage 📝

*   Define a config file (yaml) in the format below -

```yaml
<resource_name>:
    <time>: <limit>
```

As an example -

```yaml
email:
    1m: 2
    1h: 5
    1d: 6
```

Allowed time units are `s`, `m`, `h`, `d`, `w`, `M`, `y`. The time unit should be in ascending order. For example, `1m: 2, 1h: 5` is valid, but `1h: 5, 1m: 2` is not.

*   Then just use the API to check the limit and track the usage.

    *   Get usage availability

        ```bash
        curl -H "Access-ID: 123" http://localhost:8000/api/v1/usage/email
        ```

        ```json
        {
            "access_in_ms": 0
        }
        ```

        This means the user can access the resource right now.

    <!---->

    *   Register a usage

        ```bash
        curl -X POST -H "Access-ID: 123" http://localhost:8000/api/v1/usage/email
        ```

Notice that the `Access-ID` header is required. This is the unique identifier for the user or any other entity that is using the resource. This is used to track the usage for that perticular entity.

## Why Cap'em? 🤔

Say you have a resource called Email. You want to limit this email change capacity for users. This is set to twice per day. You are very happy to code with that, now the requirements come again and said twice per day but not more than one per hour, and monthly limit should be 5 🤬 Now Cap-em will come to the rescue! It's an independent service, so you can deploy in your microservices or SOA.

You can have different configurations like above or as many configs as you like with several resources. All you need is to make a config file, and use the service right away!

## Run it now! 🚀

    docker pull ananto30/cap-em
    docker run -p 8000:8000 -e DB_URI=<database_connection_url> -e CONFIG=<base64_of_config_file> ananto30/cap-em

2 environment variables are required to run the service. `DB_URI` is the database connection url. `CONFIG` is the base64 encoded config file. Check the [Makefile#L6](/Makefile#L6) to see how to encode the config file.

DB\_URI is in SQLAlchemy format. For example -
`postgresql://user:password@\<HOST>:5432/capem`

Also note that the database should be created before running the service. The service will not create the database for you. It will only create the tables.

## Available APIs 📚

*   **/api/v1/help**
    *   GET
        *   Get the help doc
*   **/api/v1/configs**
    *   GET
        *   Check the loaded configs (yaml file)
*   **/api/v1/usage/{resource\_name}**
    *   GET
        *   Get the usage availability in milliseconds
    *   POST
        *   Register a usage

## Local development 🛠

*   Setup project

    ```bash
    make setup
    ```

*   Run the service

    ```bash
    make run
    ```

### Docker 🐳

*   Build the image

    ```bash
    make docker-build
    ```
*   Run the image

    ```bash
    make docker-run
    ```

The Makefile try to get your IP and set in the `DB_URI` environment variable. If it fails, you need to set it manually.

## Tests 🧪

Tests are better to be run with SQLite database. Because there will be entries in DB and those should be cleared after each test is run. So **if you use any other than sqlite, make sure to delete the entries to pass tests**. To use SQLite you need to set the environment variable `DB_URI` -

```bash
make test
```

Custom DB -

```bash
DB_URI=sqlite:///capem-ut.db make test
```

## TODO 📝

Priority

*   A persistant way for configs? Like redis, so that multiple workers can get the same config
*   Local caching is good but how to share the configs with different workers when config get changed
*   Endpoint(s) to load/update configs, in bulk or single

Less priority

*   gRPC
*   Messaging (for event-driven services)
*   Non-relational DB support
