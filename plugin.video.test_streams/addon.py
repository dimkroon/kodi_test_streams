
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
    for name, callb in (('Small MP4 file via HTTP', 'play_short_mp4'),
                        ('Large MP4 file via HTTP', 'play_long_mp4'),
                        ):
        mnu_item = xbmcgui.ListItem(name)
        mnu_item.setProperty('IsPlayable', 'true')
        mnu_item.setInfo('video', {'mediatype': 'movie', 'title': name})
        xbmcplugin.addDirectoryItem(plugin_handle, build_url(callb), mnu_item, False)
    xbmcplugin.endOfDirectory(plugin_handle)


def play_short_mp4():
    log('PLaying mp4 over HTTP')
    play_item = xbmcgui.ListItem(
        path='https://playback.brightcovecdn.com'
             '/playback/v1/accounts/2821697655001/videos/6319726927112/high.mp4?bcov_auth=ewoJInR5cGUiOiAiSldUIiwKCSJhb'
             'GciOiAiUlMyNTYiCn0.ewoJImFjY2lkIjogIjI4MjE2OTc2NTUwMDEiCn0.XU9GEvV2NRG__OVbLn9kSt-MX5XHD6MCofzeuD2B89IQOf'
             'NYDfPPYk0ZZrQT5Lfj_PNIQh-1UsSGRjpeFu_3IJRtAf5HabobscEcBiAluTw2Vjr5WRTaNeI572h-o2zQosoQ4aNS67hl0LDGWQfAqgj'
             'f1H4EPCrQc-GvlGvoXxgpnnPHQfwLIACoN5TYOREKq26sa4wPEu1v-vWGgQBqssk9IUX2bY7ovfzY9gtec4o7pAXosZvMEiPWx3PX7pOb'
             '4s13Q6zUReHnCwofnnFewCX2QzgAAUMSqkd73iVA0VWg7Atus6Iag40mJWVoVAOgP_EXFOS76c7GJTb-rOELZw')
    play_item.setMimeType('video/mp4')
    xbmcplugin.setResolvedUrl(plugin_handle, True, listitem=play_item)


def play_long_mp4():
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
