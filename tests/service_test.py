import time

PREFIX = "/api/v1"


def test_get_config(client):
    response = client.simulate_get(f"{PREFIX}/configs")
    assert response.status == "200 OK"
    print(response.text)
    assert (
        response.text
        == """email:
  1s: 2
  5s: 5
  30s: 10

call:
  1m: 1
  5m: 5
  30d: 3"""
    )


def test_get_help(client):
    from src.api.rest import Help  # pylint: disable=import-outside-toplevel

    response = client.simulate_get(f"{PREFIX}/help")
    assert response.status == "200 OK"
    assert response.text == Help.HELP_TEXT


def test_usage_no_access_id(client):
    response = client.simulate_get(f"{PREFIX}/usage/email")
    assert response.status == "401 Unauthorized"
    assert response.json == {
        "error": "Unauthorized",
        "message": "Access-ID header is missing",
    }

    response = client.simulate_post(f"{PREFIX}/usage/email")
    assert response.status == "401 Unauthorized"
    assert response.json == {
        "error": "Unauthorized",
        "message": "Access-ID header is missing",
    }


def test_email_limit(client):
    response = client.simulate_get(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "200 OK"
    assert response.json == {"access_in_ms": 0}

    response = client.simulate_post(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "201 Created"
    response = client.simulate_post(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "201 Created"

    response = client.simulate_get(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "200 OK"
    assert response.json["access_in_ms"] > 500

    time.sleep(1)

    response = client.simulate_get(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "200 OK"
    assert response.json == {"access_in_ms": 0}

    response = client.simulate_post(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "201 Created"
    response = client.simulate_post(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "201 Created"

    # 4 times used within last 5 sec
    response = client.simulate_get(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "200 OK"
    assert response.json["access_in_ms"] > 500

    time.sleep(1)

    response = client.simulate_post(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "201 Created"

    # 5 times used within last 5 sec
    response = client.simulate_get(
        f"{PREFIX}/usage/email", headers={"Access-ID": "ananto"}
    )
    assert response.status == "200 OK"
    assert response.json["access_in_ms"] > 2500
