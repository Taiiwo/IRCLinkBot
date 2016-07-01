from threading import Thread

def thread(func, args=[], kwargs={}):
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread

def debug(msg):
    print(msg)

def missing_keys(keys, dict):
    missing_keys = []
    for key in keys:
        if key not in dict:
            missing_keys.append(key)
    return False if len(missing_keys) == 0 else missing_keys

def callback(callbacks, data):
    for callback in callbacks:
        callback(data)
