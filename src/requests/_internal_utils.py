'''Provides utility functions that are consumed internally by Requests which depend on extremely few external helpers (such as compat).'''
import re

_VALID_HEADER_NAME_RE_BYTE = re.compile(rb'^[^:\s][^:\r\n]*$')
_VALID_HEADER_NAME_RE_STR = re.compile(r'^[^:\s][^:\r\n]*$')
_VALID_HEADER_VALUE_RE_BYTE = re.compile(rb'^\S[^\r\n]*$|^$')
_VALID_HEADER_VALUE_RE_STR = re.compile(r'^\S[^\r\n]*$|^$')

_HEADER_VALIDATORS_STR = (_VALID_HEADER_NAME_RE_STR,
                          _VALID_HEADER_VALUE_RE_STR)
_HEADER_VALIDATORS_BYTE = (_VALID_HEADER_NAME_RE_BYTE,
                           _VALID_HEADER_VALUE_RE_BYTE)
HEADER_VALIDATORS = {
    bytes: _HEADER_VALIDATORS_BYTE,
    str: _HEADER_VALIDATORS_STR,
}


def to_native_string(string: str | bytes, encoding: str = 'ascii') -> str:
    """
    Convert a string-like object to a native string.

    Parameters
    ----------
    string : str | bytes
        The string-like object to convert.
    encoding : str, optional
        The encoding to use to decode the string. Defaults to 'ascii'.

    Returns
    -------
    str
        A native string.
    """
    return string if isinstance(string, str) else string.decode(encoding)


def unicode_is_ascii(u_string: str) -> bool:
    '''
    Determine if a unicode string contains only ASCII characters.

    Parameters
    ----------
    u_string : str
        Unicode string to check. Must be unicode and not Python 2 `str`.

    Returns
    -------
    bool
        `True` if `u_string` only contains ASCII characters, `False` otherwise.
    '''
    try:
        u_string.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True
