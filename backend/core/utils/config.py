from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class CoreConfig(object):
    @classmethod
    def get_default_size(cls, key='DEFAULT_PAGE_SIZE'):
        try:
            return getattr(settings, key)
        except Exception as exc:
            return ImproperlyConfigured(
                '%s is required' % key
            )

    @classmethod
    def get_default_index(cls, key='DEFAULT_PAGE_INDEX'):
        try:
            return getattr(settings, key)
        except Exception as exc:
            return ImproperlyConfigured(
                '%s is required' % key
            )

    @classmethod
    def get_start_end_index(cls, page, size):
        start = page * size
        end = start + size
        return start, end, page, size
