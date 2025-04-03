"""
Requests is an HTTP library, written in Python, for human beings.

Basic GET usage:

   >>> import requests
   >>> r = requests.get('https://www.python.org')
   >>> r.status_code
   200
   >>> b'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = requests.post('https://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key1": "value1",
       "key2": "value2"
     },
     ...
   }

The other HTTP methods are supported - see `requests.api`. Full documentation
is at <https://requests.readthedocs.io>.

:copyright: (c) 2017 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

import contextlib
import logging
import warnings
from importlib.metadata import version
from logging import NullHandler

from urllib3.exceptions import DependencyWarning

from . import packages, utils
from .__version__ import (
    __author__,
    __author_email__,
    __build__,
    __cake__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from .api import delete, get, head, options, patch, post, put, request  # type: ignore
from .exceptions import (
    ConnectionError,  # noqa: A004
    ConnectTimeout,
    FileModeWarning,
    HTTPError,
    JSONDecodeError,
    ReadTimeout,
    RequestException,
    RequestsDependencyWarning,
    Timeout,
    TooManyRedirects,
    URLRequired,
)
from .models import PreparedRequest, Request, Response
from .sessions import Session, session
from .status_codes import codes

try:
    import charset_normalizer
except ImportError:
    charset_normalizer_version = None
else:
    charset_normalizer_version = charset_normalizer.__version__

try:
    import chardet
except ImportError:
    chardet_version = None
else:
    chardet_version = chardet.__version__


def _get_version(ver: str) -> tuple[int, ...]:
    return tuple(map(int, ver))


def check_compatibility(urllib3_ver: str, chardet_ver: str | None,
                        normalizer_ver: str | None) -> None:
    _compatibility_urllib3(urllib3_ver)
    _compatibility_chardet(chardet_ver, normalizer_ver)


def _compatibility_urllib3(urllib3_ver: str) -> None:
    if 'dev' in urllib3_ver:
        msg = 'Development versions of urllib3 are not supported!'
        raise AssertionError(msg)
    urllib3_version = _get_version(urllib3_ver)
    if urllib3_version < (1, 21, 1):
        msg = f'urllib3 >= 1.21.1 is required; you have {urllib3_ver}'
        raise AssertionError(msg)


def _compatibility_chardet(chardet_ver: str | None, normalizer_ver: str | None) -> None:
    if chardet_ver:
        chardet_version = _get_version(chardet_ver)
        # chardet_version >= 3.0.2, < 6.0.0
        assert (3, 0, 2) <= chardet_version < (6, 0, 0)  # noqa: S101
    elif normalizer_ver:
        normalizer_version = _get_version(normalizer_ver)
        # charset_normalizer >= 2.0.0 < 4.0.0
        assert (2, 0, 0) <= normalizer_version < (4, 0, 0)  # noqa: S101
    else:
        warnings.warn(
            'Unable to find acceptable character detection dependency (chardet or charset_normalizer).',
            RequestsDependencyWarning,
            stacklevel=2,
        )


def _check_cryptography(cryptography_ver: str) -> None:
    cryptography_version = _get_version(cryptography_ver)
    # cryptography < 1.3.4

    if cryptography_version < (1, 3, 4):
        warning = f'Old version of cryptography ({cryptography_version}) may cause slowdown.'
        warnings.warn(warning, RequestsDependencyWarning, stacklevel=2)


urllib3_version = version('urllib3')

# Check imported dependencies for compatibility.
try:
    check_compatibility(urllib3_version, chardet_version, charset_normalizer_version)
except (AssertionError, ValueError):
    warnings.warn(
        f'urllib3 ({urllib3_version}) or chardet ({chardet_version})/charset_normalizer ({charset_normalizer_version})'
        ' doesn`t match a supported version!',
        RequestsDependencyWarning,
        stacklevel=2,
    )

# Attempt to enable urllib3's fallback for SNI support
# if the standard library doesn't support SNI or the
# 'ssl' library isn't available.
with contextlib.suppress(ImportError):
    import ssl

    from urllib3.contrib import pyopenssl

    if not getattr(ssl, 'HAS_SNI', False):
        pyopenssl.inject_into_urllib3()
        from cryptography import __version__ as cryptography_version

        _check_cryptography(cryptography_version)
warnings.simplefilter('ignore', DependencyWarning)

logging.getLogger(__name__).addHandler(NullHandler())

# FileModeWarnings go off per the default.
warnings.simplefilter('default', FileModeWarning, append=True)

__all__ = [
    'packages',
    'utils',
    '__author__',
    '__author_email__',
    '__build__',
    '__cake__',
    '__copyright__',
    '__description__',
    '__license__',
    '__title__',
    '__url__',
    '__version__',
    'delete',
    'get',
    'head',
    'options',
    'patch',
    'post',
    'put',
    'request',
    'ConnectTimeout',
    'ConnectionError',
    'HTTPError',
    'JSONDecodeError',
    'ReadTimeout',
    'RequestException',
    'Timeout',
    'TooManyRedirects',
    'URLRequired',
    'PreparedRequest',
    'Request',
    'Response',
    'Session',
    'session',
    'codes',
]
