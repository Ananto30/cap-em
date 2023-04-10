from src.stores.file_store import ConfigFileStore


class Configs:
    """
    REST resource for the configuration data.
    """

    def __init__(self, file_store: ConfigFileStore) -> None:
        self._file_store = file_store

    async def on_get(self, req, resp):  # pylint: disable=unused-argument
        """
        Get the configuration data.
        """
        file_data = self._file_store.get_configs()
        resp.data = bytes(file_data, "utf-8")
