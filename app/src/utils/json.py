import orjson


def orjson_dumps(decoded_data, *, default):
    return orjson.dumps(decoded_data, default=default).decode()
