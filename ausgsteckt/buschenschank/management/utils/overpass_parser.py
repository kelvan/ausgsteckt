import pytz
from datetime import datetime
from xml.sax import handler
from xml.sax.saxutils import unescape

DATEFORMAT = '%Y-%m-%dT%H:%M:%SZ'


class NodeCenterSaxParser(handler.ContentHandler):
    """ Extract single point elements from nodes, ways and relations from overpass xml
    Needs center tag for ways and relations
    """

    def __init__(self):
        """ fields_from_tags:
        """
        # current item
        self._item = {}
        # current position in xml is between <Item> and </Item>
        self._inItem = False
        # current subtag (No, Description, ...)
        self._currentTag = ''

    def startElement(self, name, attrs):
        if name in ['node', 'way', 'relation']:
            self._inItem = True
            self._item = {
                'id': int(attrs['id']),
                'timestamp': datetime.strptime(
                    attrs['timestamp'], DATEFORMAT
                ).replace(tzinfo=pytz.UTC),
                'user': attrs['user'],
                'tags': {}
            }

        if name in ['node', 'center']:
            self._item['lat'] = float(attrs['lat'])
            self._item['lon'] = float(attrs['lon'])

        if name == 'tag':
            self._item['tags'][attrs['k']] = unescape(attrs['v'])

        if self._inItem:
            self._currentTag = name

    def endElement(self, name):
        if name in ['node', 'way', 'relation']:
            self._inItem = False
            self._currentItem = ''
            self.process_item(self.preprocess_item(self._item))

    def preprocess_item(self, item):
        return item

    def process_item(self, item):
        """ called for every extracted item
        item: dict
        item.keys: id, lat, lon
        """
        raise NotImplementedError('save_item needs to be implemented')
