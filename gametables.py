#!/usr/bin/env python

""" gametables.py

    Randomly choose an entry from a sequence in a YAML file
"""

import argparse
import sys
import re
from string import Template
import random
import yaml


__version__ = '0.0.1'


def get_table_weights(table):
    if isinstance(table, dict) and 'table' in table:
        select = table['table']
    elif isinstance(table, list):
        select = table
    else:
        return None

    regex = r'(\d+)\*\s([\w\s]+)'

    weights = []

    for s in select:
        if isinstance(s, str):
            if (m := re.match(regex, s)):
                weights.append(int(m.group(1)))
            else:
                weights.append(1)
        else:
            weights.append(1)

    return weights


def choose_entry_from_table(table):
    '''expecting either a dist with 'table' key OR a plain list
    '''
    if isinstance(table, dict) and 'table' in table:
        select = table['table']
        end = '\n' if table.get('newline', True) else ''
    elif isinstance(table, list):
        select = table
        end = ''
    else:
        return None

    regex = r'(\d+)\*\s([\w\s]+)'

    weights = get_table_weights(table)

    choice = random.choices(select, weights=weights)[0]

    if isinstance(choice, str):
        if (m := re.match(regex, choice)):
            return m.group(2) + end
        else:
            return choice + end
    else:
        return choose_entry_from_table(choice)


def check_valid_table(table):
    '''Checks table is valid
    '''
    if not isinstance(table, dict):
        return False

    if not 'title' in table:
        return False

    if not 'table' in table:
        return False

    if 'show' in table:
        if not isinstance(table['show'], bool):
            return False

    return True


def gametables(source, target):

    # read table file
    with open(source, 'r', encoding="utf8") as s:
        table_group = [t for t in yaml.safe_load_all(s)]

    t = open(target, 'w', encoding='utf8') if target else sys.stdout

    for table in table_group:
        
        if not check_valid_table(table):
            break
        
        if table.get('show', None):
            continue
        
        result = choose_entry_from_table(table)
  
        if table.get('heading', False):
            if isinstance(table['heading'], bool):
                result = table['title'] + '\n' + result
            else:
                result = table['heading'] + '\n' + result
  
        t.write(result)

    if t is not sys.stdout:
        t.close()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Randomly choose an entry from a sequence in a YAML file")
    parser.add_argument("source", help="Source file (YAML)")
    parser.add_argument("output", help="Output file (text)", default='')
    args = parser.parse_args(args)

    gametables(args.source, args.output)


if __name__ == "__main__":
    main()
