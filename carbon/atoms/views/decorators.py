try:
    from urllib.parse import urlparse
except ImportError:     # Python 2
    from urlparse import urlparse
from functools import wraps
from django.conf import settings
from django.utils.decorators import decorator_from_middleware_with_args, available_attrs
from django.views.decorators.cache import cache_page
from django.contrib.messages.api import get_messages


def user_cache_test(test_func, cache_duration=settings.CACHE_DURATION):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            #Don't cache pages that have unique messages
            messages = get_messages(request)
            if len(messages) > 0 or test_func(request.user):

                return view_func(request, *args, **kwargs)

            else:
                return cache_page(cache_duration)(view_func)(request, *args, **kwargs) 
                

        return _wrapped_view
    return decorator


def admins_skip_cache(function=None, cache_duration=settings.CACHE_DURATION):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_cache_test(
        lambda u: u.is_authenticated() and u.is_staff,
        cache_duration=cache_duration
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def users_skip_cache(function=None, cache_duration=settings.CACHE_DURATION):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_cache_test(
        lambda u: u.is_authenticated(),
        cache_duration=cache_duration
    )
    if function:
        return actual_decorator(function)
    return actual_decorator    