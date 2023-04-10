from falcon.status_codes import HTTP_404  # pylint: disable=no-name-in-module


async def handle_404(req, resp, ex, params):  # pylint: disable=unused-argument
    resp.status = HTTP_404
    resp.body = "Not found"
