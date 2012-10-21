#    Railscasts XBMC Addon
#    -------------------
#
#    Watch screencasts from http://railscasts.com in XBMC.
#
#    :copyright: (c) 2012 by Jonathan Beluch
#    :license: GPLv3, see LICENSE.txt for more details.

from urllib2 import urlopen
from xml.dom import minidom

PLUGIN_NAME = 'Railscasts'
PLUGIN_ID = 'plugin.video.railscasts'
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

rss_feed = "http://feeds.feedburner.com/railscasts"

def get_rss():
    rss = urlopen(rss_feed)
    return rss

def get_episodes():
    rss = get_rss()

    tree = minidom.parse(rss)
    nodes = tree.childNodes

    episodes = []

    _titles = nodes.getElementsByTagName('title')
    _titles.pop(0)
    _descriptions = nodes.getElementByTagName('description')
    _descriptions.pop(0)
    _durations = nodes.getElementsByTagName('itunes:duration')
    _urls = nodes.getElementsByTagName('enclosure')

    for i in range(0, _titles.length-1):
        episodes[i] = {
            'title': _titles[i].childNodes[0].toxml() + ' (' + _durations[i].childNodes[0].toxml() + ')',
            'description': _descriptions[i].childNodes[0].toxml(),
            'url': _urls[i].getAttribute('url')
        }

    return episodes

@plugin.route('/')
def index():
    items = [
        {
            'label': episode['title'],
            'path': episode['url'],
            'info': {
                'plot': episode['description']
            },
            'is_playable': True,
        } for episode in get_episodes()
    ]

    return items

if __name__ == '__main__':
    plugin.run()