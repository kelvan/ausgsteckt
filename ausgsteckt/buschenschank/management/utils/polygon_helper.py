import logging

from django.contrib.gis.geos import Polygon

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Node:

    def __init__(self, id, lat, lon, *args, **kwargs):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.ways = {}
        self.relations = {}

    def add_way(self, way):
        self.ways[way.id] = way

    def add_membership(self, relation):
        self.relations[relation.id] = relation

    def __str__(self):
        return '[%d] %.2f %.2f' % (self.id, self.lon, self.lat)


class Way:

    def __init__(self, id, nodes, *args, **kwargs):
        self.id = id
        self.nodes = nodes
        self.relations = {}

    def __iter__(self):
        for node in self.nodes:
            yield node

    def convert_nodes(self, node_pool):
        """ Replace node id list with refernces to Node objects
        """
        for i, node in enumerate(self.nodes):
            node_obj = node_pool[node]
            self.nodes[i] = node_obj
            # Save backreference
            node_obj.add_way(self)

    def add_membership(self, relation):
        self.relations[relation.id] = relation

    def reverse(self):
        logger.debug('Reverse way %d', self.id)
        self.nodes.reverse()

    def __str__(self):
        return '[%d] %s -> %s' % (self.id, self.nodes[0], self.nodes[-1])


class Relation:

    def __init__(self, id, members, *args, **kwargs):
        self.id = id
        self.members = members

    def convert_members(self, way_pool, node_pool):
        # TODO sub relations not supported yet
        for i, member in enumerate(self.members):
            if member['type'] == 'way':
                node_obj = way_pool[member['ref']]
            elif member['type'] == 'node':
                #node_obj = node_pool[member['ref']]
                logger.warn(
                    'Node member of relation ignored'
                )
            elif member['type'] == 'relation':
                logger.warn(
                    'Sub relations not implemented yet'
                )
                continue
            else:
                logger.error(
                    'Unknown type for relation member: %s', member['type']
                )
                continue
            self.members[i] = node_obj
            # Save backreference
            node_obj.add_membership(self)

    def _get_possible_next_ways(self, last_node):
        next_ways = []
        logger.debug('Last node: %s', last_node)
        for way in last_node.ways.values():
            logger.debug('Try way %s', way)
            if way in self.members:
                if way.nodes[0] == last_node:
                    rev = False
                elif way.nodes[-1] == last_node:
                    rev = True
                else:
                    logger.info(
                        'Skip possible next way, neither first nor last'
                    )
                    continue
                next_ways.append(
                    {'way': way, 'reverse': rev}
                )
        return next_ways

    def align_members(self):
        """ Sort member ways to form a connected line
        """
        current_elem = self.members.pop()
        new_membership = [current_elem]

        for i in range(len(self.members)):
            possible_next = self._get_possible_next_ways(current_elem.nodes[-1])
            if len(possible_next) > 1:
                raise ValueError('Ambiguous next node')
            if not possible_next:
                raise ValueError('Next way not found')
            nxt = possible_next[0]
            if nxt['reverse']:
                nxt['way'].reverse()
            new_membership.append(nxt['way'])
            self.members.remove(nxt['way'])
            current_elem = nxt['way']

        self.members = new_membership


class PolygonBuilder:

    def __init__(self, data):
        self._data = data
        self._relations = []
        self._ways = {}
        self._nodes = {}
        self._sorted_nodes = []

    def prepare_data(self):
        raise NotImplementedError

    def build_polygon(self):
        polygon_coo = []

        for relation in self._relations:
            relation.align_members()
            for member in relation.members:
                polygon_coo += [(n.lon, n.lat) for n in member.nodes]

        return Polygon(polygon_coo)


class GeoJSONPolygonBuilder(PolygonBuilder):
    """ Create Polygon from geojson data
    """

    def prepare_data(self):
        for elem in self._data:
            if elem['type'] == 'node':
                self._nodes[elem['id']] = Node(**elem)

            if elem['type'] == 'way':
                self._ways[elem['id']] = Way(**elem)

            if elem['type'] == 'relation':
                self._relations.append(Relation(**elem))

        for way in self._ways.values():
            way.convert_nodes(self._nodes)
        for relation in self._relations:
            relation.convert_members(self._ways, self._nodes)
