def before(before_function):
    def decorator_func(decorated_function):
        def wrapper_func(*args, **kwargs):
            before_function(*args, **kwargs)
            return decorated_function(*args, **kwargs)
        return wrapper_func
    return decorator_func


def after(after_function):
    def decorator_func(decorated_function):
        def wrapper_func(*args, **kwargs):
            result = decorated_function(*args, **kwargs)
            after_function(*args, **kwargs)
            return result
        return wrapper_func
    return decorator_func
