'''Utility functions that are consumed internally by Requests which depend on extremely few external helpers.'''
import re

from .compat import builtin_str

_VALID_HEADER_NAME_RE_BYTE = re.compile(rb'^[^:\s][^:\r\n]*$')
_VALID_HEADER_NAME_RE_STR = re.compile(r'^[^:\s][^:\r\n]*$')
_VALID_HEADER_VALUE_RE_BYTE = re.compile(rb'^\S[^\r\n]*$|^$')
_VALID_HEADER_VALUE_RE_STR = re.compile(r'^\S[^\r\n]*$|^$')

_HEADER_VALIDATORS_STR = (_VALID_HEADER_NAME_RE_STR, _VALID_HEADER_VALUE_RE_STR)
_HEADER_VALIDATORS_BYTE = (_VALID_HEADER_NAME_RE_BYTE, _VALID_HEADER_VALUE_RE_BYTE)
HEADER_VALIDATORS = {
    bytes: _HEADER_VALIDATORS_BYTE,
    str: _HEADER_VALIDATORS_STR,
}


def to_native_string(string: str | bytes, encoding: str = 'ascii') -> builtin_str:
    '''Convert a string to the native string type.

    Parameters
    ----------
    string : str | bytes
        The string object to be converted.
    encoding : str, optional
        The encoding to use for decoding bytes, by default 'ascii'.

    Returns
    -------
    str
        The string in the native string type.
    '''
    return string if isinstance(string, str) else string.decode(encoding)


def unicode_is_ascii(u_string: str) -> bool:
    '''
    Determine if a unicode string only contains ASCII characters.

    Parameters
    ----------
    u_string : str
        Unicode string to check. Must be a Python 3 `str`.

    Returns
    -------
    bool
        True if all characters are ASCII, False otherwise.
    '''
    assert isinstance(u_string, str)  # noqa: S101
    return u_string.isascii()
