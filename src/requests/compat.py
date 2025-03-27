'''
Module previously handled import compatibility issues between Python 2 and Python 3.

It remains for backwards compatibility until the next major version.
'''
import contextlib
import importlib
import sys
from collections import OrderedDict
from collections.abc import Callable, Mapping, MutableMapping
from http import cookiejar as cookielib
from http.cookies import Morsel
from io import StringIO
from types import ModuleType
from urllib.parse import (
    quote,
    quote_plus,
    unquote,
    unquote_plus,
    urldefrag,
    urlencode,
    urljoin,
    urlparse,
    urlsplit,
    urlunparse,
)
from urllib.request import (
    getproxies,
    getproxies_environment,
    parse_http_list,
    proxy_bypass,
    proxy_bypass_environment,
)

# -------
# urllib3
# -------
from urllib3 import __version__ as urllib3_version

# Detect which major version of urllib3 is being used.
try:
    is_urllib3_1 = int(urllib3_version.split('.')[0]) == 1
except (TypeError, AttributeError):
    # If we can't discern a version, prefer old functionality.
    is_urllib3_1 = True

# -------------------
# Character Detection
# -------------------


def _resolve_char_detection() -> ModuleType | None:
    '''Resolve the character detection module.

    Returns
    -------
    ModuleType | None
        Resolve the character detection module.
    '''
    for lib in ('chardet', 'charset_normalizer'):
        with contextlib.suppress(ImportError):
            return importlib.import_module(lib)
    return None


chardet = _resolve_char_detection()

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = _ver[0] == 2

#: Python 3.x?
is_py3 = _ver[0] == 3

# json/simplejson module import resolution


json = importlib.import_module('simplejson', 'json')
JSONDecodeError = getattr(json, 'JSONDecodeError', importlib.import_module('json').JSONDecodeError)

# Keep OrderedDict for backwards compatibility.


# --------------
# Legacy Imports
# --------------


builtin_str = str
basestring = (str, bytes)
numeric_types = (int, float)
integer_types = (int, )
__all__ = [
    'json',
    'JSONDecodeError',
    'OrderedDict',
    'Morsel',
    'cookielib',
    'Callable',
    'Mapping',
    'MutableMapping',
    'StringIO',
    'basestring',
    'builtin_str',
    'getproxies',
    'getproxies_environment',
    'parse_http_list',
    'proxy_bypass',
    'proxy_bypass_environment',
    'quote',
    'quote_plus',
    'unquote',
    'unquote_plus',
    'urldefrag',
    'urlencode',
    'urljoin',
    'urlparse',
    'urlsplit',
    'urlunparse',
]
