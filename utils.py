from copy import deepcopy
from functools import wraps


def add_operation(before: list = [], after: list = []):
    def add_operation_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            for before_fuc in before:
                before_fuc(*args, **kwargs)

            res = func(*args, **kwargs)

            for after_fuc in after:
                after_fuc(*args, **kwargs)

            return res

        return wrapper

    return add_operation_decorator


def update_func(origin, before: list = [], after: list = []):

    origin = deepcopy(origin)

    @add_operation(before, after)
    def new_func(*args, **kwargs):
        origin(*args, **kwargs)

    return new_func
