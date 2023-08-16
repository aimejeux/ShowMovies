# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.11 (v2.7.11:6d1b6a68f775, Dec  5 2015, 20:40:30) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/lib/player/m3u8player/m3u8/parser.py
# Compiled at: 2018-05-11 05:07:28
"""
M3U8 parser.

"""
import re
from collections import namedtuple
ext_x_targetduration = '#EXT-X-TARGETDURATION'
ext_x_media_sequence = '#EXT-X-MEDIA-SEQUENCE'
ext_x_key = '#EXT-X-KEY'
ext_x_stream_inf = '#EXT-X-STREAM-INF'
ext_x_version = '#EXT-X-VERSION'
ext_x_allow_cache = '#EXT-X-ALLOW-CACHE'
ext_x_endlist = '#EXT-X-ENDLIST'
extinf = '#EXTINF'
ext_x_program_date_time = '#EXT-X-PROGRAM-DATE-TIME'
ATTRIBUTELISTPATTERN = re.compile('((?:[^,"\']|"[^"]*"|\'[^\']*\')+)')

def parse(content):
    """
    Given a M3U8 playlist content returns a dictionary with all data found
    """
    data = {'is_variant': False, 
       'is_endlist': False, 
       'playlists': [], 'segments': []}
    state = {'expect_segment': False, 
       'expect_playlist': False}
    for line in string_to_lines(content):
        line = line.strip()
        if line.startswith(ext_x_targetduration):
            _parse_simple_parameter(line, data, float)
        elif line.startswith(ext_x_media_sequence):
            _parse_simple_parameter(line, data, int)
        elif line.startswith(ext_x_version):
            _parse_simple_parameter(line, data)
        elif line.startswith(ext_x_allow_cache):
            _parse_simple_parameter(line, data)
        elif line.startswith(ext_x_key):
            _parse_key(line, data)
        elif line.startswith(extinf):
            _parse_extinf(line, data, state)
            state['expect_segment'] = True
        elif line.startswith(ext_x_program_date_time):
            if state['expect_segment']:
                _parse_simple_parameter(line, state)
        elif line.startswith(ext_x_stream_inf):
            state['expect_playlist'] = True
            _parse_stream_inf(line, data, state)
        elif line.startswith(ext_x_endlist):
            data['is_endlist'] = True
        elif state['expect_segment']:
            _parse_ts_chunk(line, data, state)
            state['expect_segment'] = False
        elif state['expect_playlist']:
            _parse_variant_playlist(line, data, state)
            state['expect_playlist'] = False

    return data


def _parse_key(line, data):
    params = ATTRIBUTELISTPATTERN.split(line.replace(ext_x_key + ':', ''))[1::2]
    data['key'] = {}
    for param in params:
        name, value = param.split('=', 1)
        data['key'][normalize_attribute(name)] = remove_quotes(value)


def _parse_extinf(line, data, state):
    val = line.replace(extinf + ':', '').split(',')
    if len(val) > 1:
        title = val[1]
    else:
        title = ''
    state['segment'] = {'duration': float(val[0]), 'title': remove_quotes(title)}


def _parse_ts_chunk(line, data, state):
    segment = state.pop('segment')
    segment['uri'] = line
    data['segments'].append(segment)


def _parse_stream_inf(line, data, state):
    params = ATTRIBUTELISTPATTERN.split(line.replace(ext_x_stream_inf + ':', ''))[1::2]
    stream_info = {}
    for param in params:
        name, value = param.split('=', 1)
        stream_info[normalize_attribute(name)] = value

    if 'codecs' in stream_info:
        stream_info['codecs'] = remove_quotes(stream_info['codecs'])
    data['is_variant'] = True
    state['stream_info'] = stream_info


def _parse_variant_playlist(line, data, state):
    playlist = {'uri': line, 'stream_info': state.pop('stream_info')}
    data['playlists'].append(playlist)


def _parse_simple_parameter(line, data, cast_to=str):
    param, value = line.split(':', 1)
    param = normalize_attribute(param.replace('#EXT-X-', ''))
    value = normalize_attribute(value)
    data[param] = cast_to(value)


def string_to_lines(string):
    return string.strip().replace('\r\n', '\n').split('\n')


def remove_quotes(string):
    """
    Remove quotes from string.

    Ex.:
      "foo" -> foo
      'foo' -> foo
      'foo  -> 'foo

    """
    quotes = ('"', "'")
    if string and string[0] in quotes and string[(-1)] in quotes:
        return string[1:-1]
    return string


def normalize_attribute(attribute):
    return attribute.replace('-', '_').lower().strip()


def is_url(uri):
    return re.match('https?://', uri) is not None
# okay decompiling F:\TSMstudio\bin\release\scripts\main\lib\m3u8player\m3u8\parser.pyo
