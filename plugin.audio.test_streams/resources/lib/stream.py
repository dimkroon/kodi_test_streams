# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

from __future__ import annotations
import re
import json
import requests
import xbmc
import xbmcgui


WEB_TIMEOUT = (3.5, 3)
MEDIA_SELECTOR_URL = ('https://open.live.bbc.co.uk/mediaselector/6/select/version/3.0/'
                      'mediaset/pc/cvid/urn:bbc:pips:pid:{}/format/json/cors/1')


def play_on_demand(service_id) -> xbmcgui.ListItem | None:
    """Play an on-demand stream"""
    xbmc.log('play on demand: service_id = "%s".' % service_id)
    strm_url = select_stream_url(service_id)
    li = create_dash_listitem(strm_url)
    return li


def play_live(service_id: str) -> xbmcgui.ListItem | None:
    """Play a live stream

    Play from the start time if `start_t` is provided.

    """
    jwt = get_jwt('https://www.bbc.co.uk/sounds/play/live/' + service_id)
    strm_url = select_stream_url(service_id, jwt)
    li = create_dash_listitem(strm_url)
    return li


def get_jwt(url) -> str | None:
    """Get the JWT required for live streams."""
    resp = requests.get(url, timeout=WEB_TIMEOUT)
    resp.raise_for_status()
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', resp.text, re.DOTALL)
    if not match:
        return None
    json_data = json.loads(match[1])
    tkn = json_data['props']['pageProps'].get('jwtToken')
    return tkn


def select_stream_url(media_id: str,
                      jwt: str | None = None) -> str | None:
    """Request the stream selector and select the dash stream with the highest bitrate."""
    url = MEDIA_SELECTOR_URL.format(media_id)
    if jwt:
        headers = {'authorization': 'Bearer ' + jwt}
    else:
        headers = None
    resp = requests.get(url, headers=headers, timeout=WEB_TIMEOUT)
    if resp.status_code in (401, 403):
        xbmc.log(f'[BBC Sounds Test Streams] HTTP Error {resp.status_code} on playlist request:\n{resp.text}')
        xbmc.log(f'[BBC Sounds Test Streams] My ip is {requests.get("https://api.myip.com").text}')
    resp.raise_for_status()
    streams_data = json.loads(resp.content)
    selected_media_set = {}
    highest_bitrate = 0

    try:
        for media_set in streams_data['media']:
            # Note: some streams include non-audio streams like captions.
            kind = media_set.get('kind')
            if kind == 'audio':
                if media_set.get('bitrate', 0) > highest_bitrate:
                    selected_media_set = media_set

        for connection in selected_media_set['connection']:
            if connection['protocol'] == 'https' and connection['transferFormat'] == 'dash':
                return connection['href']
    except KeyError as err:
        xbmc.log('[BBC Sounds Test Streams] Error parsing streams data: %r\n%s' % (err, streams_data), xbmc.LOGERROR)
    return None


def create_dash_listitem(url) -> xbmcgui.ListItem:
    li = xbmcgui.ListItem(path=url, offscreen=True)
    li.setProperty("IsPlayable", "true")
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setMimeType('application/dash+xml')
    li.setContentLookup(False)
    return li
