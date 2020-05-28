import time
from base import Session
from history import History

# Config line: email, 60:1, 3600:2, 86400:5
# Query: email, ananto

session = Session()
config_map = {}


def request(config, access_id):
    req_time = time.time()

    for cfg in config_map[config]:
        start_time = req_time - cfg[0]
        c = session.query(History)\
            .filter(History.access_id == access_id)\
            .filter(History.access_at >= start_time)\
            .count()
        print(c)
        if c >= cfg[1]:
            return False

    new_record = History(
        access_id=access_id,
        resource_name=config,
        access_at=req_time
    )
    session.add(new_record)
    session.commit()

    return True


def make_config():
    # TODO: read config from file
    config_map['email'] = [(60, 1), (3600, 2), (86400, 5)]


make_config()
while True:
    x = input().split(',')
    print(request(x[0], x[1]))
