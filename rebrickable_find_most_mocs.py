#!/usr/bin/env python3
"""
Script to find which LEGO sets have the most MOCs for them.
"""

import argparse
import operator
from queue import Queue
from threading import Thread
import urllib

from rebrickable import Rebrickable

import rebrickable_find_most_mocs_conf

DEFAULT_OUTPUTDIR = '.'

concurrent = 10

counts = []
q = Queue(concurrent * 2)

def worker():
    while True:
        set = q.get()
        try:
            num_mocs = rebrickable.get_num_mocs_for_set(set)
        except urllib.error.URLError:
            print("Getting num mocs for %s failed" % (set['set_id'],))
            raise
        print("Got mocs for %s, count=%d" % (set['set_id'], num_mocs,))
        counts.append((set, num_mocs,))
        q.task_done()

for i in range(concurrent):
    t = Thread(target=worker)
    t.daemon = True
    t.start()


def rebrickable_find_most_mocs(rebrickable_api_key, year):
    """
    Find which LEGO sets have the most MOCs

    :param rebrickable_api_key: Rebrickable.com API key
    :return: nothing
    """

    global rebrickable

    if rebrickable_api_key is None:
        rebrickable_api_key = rebrickable_find_most_mocs_conf.get_rebrickable_api_key()
        if rebrickable_api_key is None:
            raise Exception('No Rebrickable API key in {0} or on command line'.format(
                rebrickable_find_most_mocs_conf.CONF_FILE_NAME))
    rebrickable = Rebrickable(rebrickable_api_key)
 
    sets = rebrickable.get_all_sets(year, year)
    print("num sets total=%s" % (len(sets),))

    for set in sets:
        q.put(set)
    q.join()

    counts.sort(key=operator.itemgetter(1))
    for set, num_mocs in counts:
        if num_mocs >= 2:
            print('%s %s (%s pieces)' % (set['descr'], set['url'], set['pieces'],))


def main():
    """
    Main-entry point. Parse command-line arguments then call rebrickable_find_most_mocs

    :return: nothing
    """
    parser = argparse.ArgumentParser(description='Find which LEGO sets have the most MOCs')
    parser.add_argument('year', help='the year to search')
    parser.add_argument('-r', '--rebrickable_api_key', metavar='REBRICKABLE_API_KEY',
                        help='Rebrickable API key (overrides value in conf file')
    args = parser.parse_args()

    rebrickable_find_most_mocs(args.rebrickable_api_key, args.year)

if __name__ == '__main__':
    main()
