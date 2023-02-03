
#  Copyright (c) 2022 Dimitri Kroon.
#
#  SPDX-License-Identifier: GPL-2.0-or-later

import sys
import inspect

import xbmc
import xbmcplugin
import xbmcgui


def log(message):
    xbmc.log('[TEST_STREAMS] ' + message, xbmc.LOGDEBUG)


def build_url(callb):
    return '{}?{}'.format(plugin_url, callb)


def menu():
    log('Showing menu')
    xbmcplugin.setContent(plugin_handle, 'videos')
    for name, callb in (('DASH/WD OK', 'play_dash_wd_ok'),
                        ('DASH/WD malformed stream headers - plays OK', 'play_malformed_stream_header'),
                        ('DASH/WD malformed key request headers - crashes', 'play_malformed_keyreq_header'),
                        ('MP4 file via HTTP', 'play_mp4')):
        mnu_item = xbmcgui.ListItem(name)
        mnu_item.setProperty('IsPlayable', 'true')
        mnu_item.setInfo('video', {'mediatype': 'movie', 'title': name})
        xbmcplugin.addDirectoryItem(plugin_handle, build_url(callb), mnu_item, False)
    xbmcplugin.endOfDirectory(plugin_handle)


def create_playitem():
    # from https://shaka-player-demo.appspot.com/demo/
    url = 'https://storage.googleapis.com/shaka-demo-assets/sintel-widevine/dash.mpd'

    li = xbmcgui.ListItem(path=url)
    li.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    li.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setMimeType('application/dash+xml')
    li.setContentLookup(False)
    return li


def play_dash_wd_ok():
    log('PLaying DASH+WD')
    play_item = create_playitem()
    play_item.setProperty('inputstream.adaptive.stream_headers', 'Pragma=no-cache&DNT=1')
    play_item.setProperty('inputstream.adaptive.license_key',
                          'https://cwip-shaka-proxy.appspot.com/no_auth|Pragma=no-cache|R{SSM}|')
    xbmcplugin.setResolvedUrl(plugin_handle, True, listitem=play_item)


def play_malformed_stream_header():
    log('PLaying DASH+WD with malformed stream headers')
    play_item = create_playitem()
    # Stream Headers has a trailing '&', still plays OK
    play_item.setProperty('inputstream.adaptive.stream_headers', 'Pragma=no-cache&')
    play_item.setProperty('inputstream.adaptive.license_key',
                          'https://cwip-shaka-proxy.appspot.com/no_auth|Pragma=no-cache|R{SSM}|')
    xbmcplugin.setResolvedUrl(plugin_handle, True, listitem=play_item)


def play_malformed_keyreq_header():
    log('PLaying DASH+WD with malformed key request headers')
    play_item = create_playitem()
    # License key headers has a trailing '&', kodi crashes
    play_item.setProperty('inputstream.adaptive.license_key', 'https://cwip-shaka-proxy.appspot.com/no_auth||R{SSM}|')
    xbmcplugin.setResolvedUrl(plugin_handle, True, listitem=play_item)


def play_mp4():
    log('PLying mp4 over HTTP')
    play_item = xbmcgui.ListItem(path='https://twit.cachefly.net/video/twit/twit0811/twit0811_h264m_1280x720_1872.mp4')
    play_item.setMimeType('video/mp4')
    xbmcplugin.setResolvedUrl(plugin_handle, True, listitem=play_item)


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
