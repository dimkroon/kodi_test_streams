import json
#  Copyright (c) 2022 Dimitri Kroon.
#
#  SPDX-License-Identifier: GPL-2.0-or-later

import sys
import inspect

import xbmc
import xbmcplugin
import xbmcgui


DOC = 'no continue watching items'
MSG = 'Expecting value'


def log(message):
    xbmc.log('[TEST_SIMPLEJSON_CRASH] ' + message, xbmc.LOGINFO)


def build_url(callb):
    return '{}?{}'.format(plugin_url, callb)


def menu():
    log('Showing menu')
    xbmcplugin.setContent(plugin_handle, 'videos')
    for name, callb in (('Test str.count()', 'test_str_count'),
                        ('Build error message', 'test_build_msg'),
                        ('Create simplejson Exception', 'test_simplejson_exc'),
                        ('Create standard json Exception', 'test_stdjson_exc'),
                        ("Test simplejson.loads()", 'test_simpjson_loads'),
                        ("Test standard json.loads()", 'test_std_json_loads'),
                        ("Test requests' response.jons()", 'test_resp_json'),
                        ("Test unhandled JSONDecodeError", 'test_unhandled_json_error')
                        ):
        mnu_item = xbmcgui.ListItem(name)
        mnu_item.setProperty('IsPlayable', 'true')
        # mnu_item.setInfo('video', {'mediatype': 'movie', 'title': name})
        xbmcplugin.addDirectoryItem(plugin_handle, build_url(callb), mnu_item, False)
    xbmcplugin.endOfDirectory(plugin_handle)


def test_str_count():
    log('Testing str.count()...')
    lineno = DOC.count('\n', 0, 0) + 1
    xbmcplugin.endOfDirectory(plugin_handle)
    log('Testing str.count() succeeded')
    xbmcgui.Dialog().ok('Tests', 'Testing str.count()... OK')


def test_build_msg():
    log('Testing build error message...')
    from simplejson.errors import errmsg
    full_msg = errmsg(MSG, DOC, 0)
    xbmcplugin.endOfDirectory(plugin_handle)
    log('Testing build error message succeeded')
    xbmcgui.Dialog().ok('Tests', 'Testing build error message... OK')


def test_simplejson_exc():
    log('Testing create simplejson exception...')
    from simplejson.errors import JSONDecodeError
    exc = JSONDecodeError(MSG, DOC, 0)
    xbmcplugin.endOfDirectory(plugin_handle)
    log('Testing create simplejson exception succeeded')
    xbmcgui.Dialog().ok('Tests', 'Testing create simplejson exception... OK')


def test_stdjson_exc():
    log('Testing create standard json exception...')
    from json import JSONDecodeError
    exc = JSONDecodeError(MSG, DOC, 0)
    xbmcplugin.endOfDirectory(plugin_handle)
    log('Testing create standard json exception succeeded')
    xbmcgui.Dialog().ok('Tests', 'Testing create standard json exception... OK')


def test_simpjson_loads():
    log('Testing simplejson.loads()...')
    import simplejson
    try:
        simplejson.loads(DOC)
    except simplejson.JSONDecodeError:
        log('Testing simplejson.loads() succeeded')
        xbmcgui.Dialog().ok('Tests', 'Testing simplejson.loads()... OK')
    else:
        log('Testing simplejson.loads() failed: no exception raised')
        xbmcgui.Dialog().ok('Tests', 'Testing simplejson.loads()... Failed')
    xbmcplugin.endOfDirectory(plugin_handle)


def test_std_json_loads():
    log('Testing standard json.loads()...')
    import json
    try:
        json.loads(DOC)
    except json.JSONDecodeError:
        log('Testing standard json.loads() succeeded')
        xbmcgui.Dialog().ok('Tests', 'Testing standard json.loads()... OK')
    else:
        log('Testing standard json.loads() failed: no exception raised')
        xbmcgui.Dialog().ok('Tests', 'Testing standard json.loads()... Failed')
    xbmcplugin.endOfDirectory(plugin_handle)


def test_resp_json():
    from requests import compat
    if compat.JSONDecodeError is json.JSONDecodeError:
        log('Testing response.json() using std json ...')
    else:
        log('Testing response.json() using simplejson ...')
    from requests.models import Response
    mocked_response = Response()
    mocked_response._content = DOC.encode('utf8')
    try:
        data = mocked_response.json()
    except requests.JSONDecodeError:
        log('Testing response.json() succeeded')
        xbmcgui.Dialog().ok('Tests', 'Testing response.json()... OK')
    else:
        log('Testing response.json() failed: no exception raised')
        xbmcgui.Dialog().ok('Tests', 'Testing response.json()... Failed')
    xbmcplugin.endOfDirectory(plugin_handle)


def test_unhandled_json_error():
    from requests import compat
    if compat.JSONDecodeError is json.JSONDecodeError:
        log('Testing unhandled JSONDecodeError using std json ...')
    else:
        log('Testing unhandled JSONDecodeError using simplejson ...')
    from requests.models import Response
    mocked_response = Response()
    mocked_response._content = DOC.encode('utf8')
    data = mocked_response.json()
    log('Testing unhandled JSONDecodeError failed: no exception raised')
    xbmcgui.Dialog().ok('Tests', 'Testing requests.reponse.json()... Failed')
    xbmcplugin.endOfDirectory(plugin_handle)


log("Python version: {}".format(sys.version))
log("Python executable: {}".format(sys.executable))
log("sys args = {}".format(sys.argv))
plugin_url = sys.argv[0]
plugin_handle = int(sys.argv[1])

func_name = sys.argv[2][1:]
funcs = {name: member for name, member in inspect.getmembers(sys.modules[__name__])
         if (inspect.isfunction(member))}
callb = funcs.get(func_name)
if callb:
    callb()
else:
    menu()
