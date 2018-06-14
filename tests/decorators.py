"""
These are decorators to help make testing
using pytest and flask easy
"""
from posixpath import join

from decorator import decorator


def request_context(route, app_pos=0, **route_args):
    """
    Wrap a request in a request context with any other needed information.
    app_pos is the position of the flask app argument
    """
    @decorator
    def func_wrapper(func, *args, **kwargs):
        """
        Do the function call in an app & request context
        """
        app = args[app_pos]
        with app.app_context():
            with app.test_request_context(route, **route_args):
                return func(*args, **kwargs)
    return func_wrapper


def request_context_from_args(route, app_pos=0, uuid_pos=1, **route_args):
    """
    Wrap a request in a request context with any other needed information.
    app_pos is the position of the flask app argument, and uuid_pos is
    the position of the uuid argument, and route is both of them joined.
    """
    @decorator
    def func_wrapper(func, *args, **kwargs):
        """
        Do the function call in an app & request context
        """
        app = args[app_pos]
        uuid = args[uuid_pos]
        with app.app_context():
            with app.test_request_context(join(route, uuid), **route_args):
                return func(*args, **kwargs)
    return func_wrapper


def flask_context(app_pos=0):
    """
    Wrap a request in a flask context
    app_pos is the position of the flask app argument
    """
    @decorator
    def func_wrapper(func, *args, **kwargs):
        """
        Do the function call in an app context
        """
        app = args[app_pos]
        with app.app_context():
            return func(*args, **kwargs)
    return func_wrapper
