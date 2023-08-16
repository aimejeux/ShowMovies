# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.11 (v2.7.11:6d1b6a68f775, Dec  5 2015, 20:40:30) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/lib/player/m3u8player/m3u8/__init__.py
# Compiled at: 2018-05-11 05:07:28
import os, re, urlparse
from urllib2 import urlopen
from model import M3U8, Playlist
from parser import parse, is_url
__all__ = ('M3U8', 'Playlist', 'loads', 'load', 'parse')

def inits(content, uri):
    """
    Given a string with a m3u8 content and uri from which 
    this content was downloaded returns a M3U8 object.
    Raises ValueError if invalid content
    """
    parsed_url = urlparse.urlparse(uri)
    prefix = parsed_url.scheme + '://' + parsed_url.netloc
    base_path = os.path.normpath(parsed_url.path + '/..')
    base_uri = urlparse.urljoin(prefix, base_path)
    return M3U8(content, base_uri=base_uri)


def loads(content):
    """
    Given a string with a m3u8 content, returns a M3U8 object.
    Raises ValueError if invalid content
    """
    return M3U8(content)


def load(uri):
    """
    Retrieves the content from a given URI and returns a M3U8 object.
    Raises ValueError if invalid content or IOError if request fails.
    """
    if is_url(uri):
        return _load_from_uri(uri)
    else:
        return _load_from_file(uri)


def _load_from_uri(uri):
    open = urlopen(uri)
    uri = open.geturl()
    content = open.read().strip()
    parsed_url = urlparse.urlparse(uri)
    prefix = parsed_url.scheme + '://' + parsed_url.netloc
    base_path = os.path.normpath(parsed_url.path + '/..')
    base_uri = urlparse.urljoin(prefix, base_path)
    return M3U8(content, base_uri=base_uri)


def _load_from_file(uri):
    with open(uri) as (fileobj):
        raw_content = fileobj.read().strip()
    base_uri = os.path.dirname(uri)
    return M3U8(raw_content, base_uri=base_uri)
# okay decompiling F:\TSMstudio\Engine\__init__.pyo
