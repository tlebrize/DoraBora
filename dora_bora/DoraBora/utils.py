from functools import wraps

from django.apps import apps


def get_model(*args, **kwargs):
    """
    This function can be used to lazily load a django model, it will be loaded as late as possible.
    This is mostly usefull to prevent circular imports.
    """

    class LazyCache:
        def __getattr__(self, name):
            return getattr(apps.get_model(*args, **kwargs), name)

        def __call__(self, *init_args, **init_kwargs):
            return apps.get_model(*args, **kwargs)(*init_args, **init_kwargs)

    return LazyCache()
