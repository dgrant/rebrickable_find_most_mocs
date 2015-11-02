"""
Rebrickable API.
"""
import collections
import json

from pycommon.http import do_http_get


class Rebrickable(object):
    """
    Rebrickable API.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def get_all_sets(self, min_year, max_year):
        """
        Return the total number of parts found on Rebrickable.com for the part id
        :param part_id: a lego part id
        :return: the total number of parts found for the given part id
        """
        result = do_http_get('http://rebrickable.com/api/search',
                             params=collections.OrderedDict(
                                          {'key': self.api_key, 'type': 'S', 'format': 'json',
                                           'min_year': min_year, 'max_year': max_year}))

        return [x for x in json.loads(result)['results']]

    def get_num_mocs_for_set(self, s):
        set_id = s['set_id']

        result = do_http_get('http://rebrickable.com/api/get_alt_builds',
                             params=collections.OrderedDict(
                                          {'key': self.api_key, 'set_id': set_id, 'format': 'json'}))

        return len(json.loads(result))
