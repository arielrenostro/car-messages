from functools import wraps

from car_message.raspberry.connector import connector


def handle_exception(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            connector.close()
            print(str(e))
    return wrapper
