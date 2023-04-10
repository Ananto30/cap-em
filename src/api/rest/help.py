class Help:
    """
    Returns the help.
    """

    HELP_TEXT = """
Welcome to cap-em!

APIs:
----
- GET /api/v1/usage/<resource_name> --header "Access-ID: <access_id>"
    This will return the number of milliseconds until the next request can be made.

    Example:
    $ curl -H "Access-ID: 123" http://localhost:8000/api/v1/usage/email
    $ {"access_in_ms": 3000}

- POST /api/v1/usage/<resource_name> --header "Access-ID: <access_id>"
    This will add a new usage record.

    Example:
    $ curl -X POST -H "Access-ID: 123" http://localhost:8000/api/v1/usage/email
    $ 201 Created

- GET /api/v1/configs
    This will return the configuration data.

    Example:
    $ curl http://localhost:8000/api/v1/configs
    $ email:
    $   1m: 3
    $   5m: 10
    $   1h: 20

Headers:
-------
- Access-ID: <access_id>
    This is the unique identifier for the user or any other entity
    for which the usage is being tracked.
    This is a required header for the usage APIs.
"""

    def __init__(self) -> None:
        pass

    async def on_get(self, req, resp):  # pylint: disable=unused-argument
        """
        Get the help.
        """
        resp.data = bytes(self.HELP_TEXT, "utf-8")
