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
    """
    Add some processing before and after the execution of the original function. Returns a new function.

    This function contains the following parameters

    origin:     The original function
    before:     A list of functions. These functions will be executed !!before!! the original function
    after:      A list of functions. These functions will be executed !!after!! the original function
    """

    origin = deepcopy(origin)

    @add_operation(before, after)
    @wraps(origin)
    def new_func(*args, **kwargs):
        origin(*args, **kwargs)

    return new_func

def count_pattern(string, pattern):
    res_of_count = string.count(pattern)
    return res_of_count


if __name__ == '__main__':
    string = "abcdefgaaaa"
    pattern = "a"
    count_ans = count_pattern(string, pattern)
    print(count_ans)