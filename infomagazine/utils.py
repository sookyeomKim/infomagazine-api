import collections
from functools import wraps

from rest_framework.response import Response


def split_env(env: str) -> list:
    return env.split(',')


class ReturnValuesFormatter:
    def __init__(self):
        self._values_to_return = None

    @property
    def values_to_return(self):
        return self._values_to_return

    @values_to_return.setter
    def values_to_return(self, set_values):
        values_to_return_named_tuple = collections.namedtuple('values_to_return',
                                                              ['state',
                                                               'data',
                                                               'message',
                                                               'options'])
        self._values_to_return = values_to_return_named_tuple(**set_values)

    def generate(self):
        formatted_values = {
            'data':
                {
                    'state': self._values_to_return.state,
                    'data': self._values_to_return.data,
                    'message': self._values_to_return.message
                }
        }
        formatted_values.update(self._values_to_return.options)
        return formatted_values


def response_decorator(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        data = func(*args, **kwargs)
        response_formatter = ReturnValuesFormatter()

        response_formatter.values_to_return = {
            'state': data['state'],
            'data': data['data'],
            'message': data['message'],
            'options': data['options']
        }

        return Response(**response_formatter.generate())

    return decorator

# def response_decorator(param):
#     def wrapper(func):
#         @wraps(func)
#         def decorator(*args, **kwargs):
#             data = func(*args, **kwargs)
#             response_formatter = ReturnValuesFormatter()
#
#             response_formatter.values_to_return = {
#                 'state': data['state'],
#                 'data': data['data'],
#                 'message': data['message'],
#                 'options': data['options']
#             }
#             return Response(**response_formatter.generate())
#
#         return decorator
#
#     return wrapper
