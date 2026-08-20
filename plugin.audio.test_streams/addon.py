
#  Copyright (c) 2022 Dimitri Kroon.
#
#  SPDX-License-Identifier: GPL-2.0-or-later

import os
import sys
import inspect

import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

from resources.lib import stream


ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')

def log(message):
    xbmc.log('[TEST_STREAMS] ' + message, xbmc.LOGDEBUG)


def build_url(callb):
    return '{}?{}'.format(plugin_url, callb)


def menu():
    log('Showing menu')
    xbmcplugin.setContent(plugin_handle, 'videos')
    for name, callb in (('BBC Radio 1 live - dash', 'radio_dash'),
                        ('BBC Audio on demand - dash', 'on_demand_dash'),
                        ):
        mnu_item = xbmcgui.ListItem(name)
        mnu_item.setProperty('IsPlayable', 'true')
        mnu_item.setInfo('video', {'mediatype': 'episode', 'title': name})
        xbmcplugin.addDirectoryItem(plugin_handle, build_url(callb), mnu_item, False)
    xbmcplugin.endOfDirectory(plugin_handle)


def radio_dash():
    li = stream.play_live('bbc_radio_one')
    xbmcplugin.setResolvedUrl(plugin_handle, True, listitem=li)


def on_demand_dash():
    sid = 'p0p0mgpt'
    li = stream.play_on_demand(sid)
    xbmcplugin.setResolvedUrl(plugin_handle, True, listitem=li)


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
