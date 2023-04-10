import logging

from falcon import HTTP_201, HTTP_401

from src.stores.usage_store import UsageStore


class Usage:
    """
    REST resource for the usage tracking.
    """

    def __init__(self, usage_store: UsageStore) -> None:
        self._usage_store = usage_store

    async def on_get(self, req, resp, resource_name):
        """
        Get the available usage of the resource.
        """
        access_id = req.get_header("Access-ID")
        if access_id is None:
            resp.status = HTTP_401
            resp.media = {
                "error": "Unauthorized",
                "message": "Access-ID header is missing",
            }
            return

        access_in_ms = self._usage_store.get_usage(resource_name, access_id)
        resp.media = {"access_in_ms": access_in_ms}

    async def on_post(self, req, resp, resource_name):
        """
        Add a new usage record.
        """
        access_id = req.get_header("Access-ID")
        if access_id is None:
            resp.status = HTTP_401
            resp.media = {
                "error": "Unauthorized",
                "message": "Access-ID header is missing",
            }
            return

        self._usage_store.add_usage(resource_name, access_id)

        logging.info(
            "Added usage record",
            extra={
                "resource_name": resource_name,
                "access_id": access_id,
            },
        )

        resp.status = HTTP_201
