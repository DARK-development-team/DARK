import os


def preserve_cwd():
    def decorator_func(decorated_function):
        def wrapper_func(*args, **kwargs):
            cwd = os.getcwd()
            result = decorated_function(*args, **kwargs)
            os.chdir(cwd)
            return result
        return wrapper_func
    return decorator_func


def data_path():
    return 'dark/data'
