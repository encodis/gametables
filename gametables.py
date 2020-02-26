#!/usr/bin/env python

""" gametables.py

    Randomly choose an entry from a sequence in a YAML file
"""

import argparse
import sys
import re
import random
import yaml


__version__ = '0.0.1'


TABLE_GROUP = {}
TABLE_RECURSION_COUNT = 0

MAX_TABLE_RECURSION = 20


def get_table_weights(table):
    if isinstance(table, dict) and 'table' in table:
        select = table['table']
    elif isinstance(table, list):
        select = table
    else:
        return None

    weight_re = r'(\d+)\*\s([\w\s]+)'

    weights = []

    for s in select:
        if isinstance(s, str):
            if (m := re.match(weight_re, s)):
                weights.append(int(m.group(1)))
            else:
                weights.append(1)
        else:
            weights.append(1)

    return weights


def choose_entry_from_table(table):
    '''expecting either a dist with 'table' key, a plain list or an RE match object
    '''
    
    global TABLE_RECURSION_COUNT
    TABLE_RECURSION_COUNT += 1
            
    if TABLE_RECURSION_COUNT > MAX_TABLE_RECURSION:
        return ''
    
    if isinstance(table, dict) and 'table' in table:
        # table, dict with 'table' element
        select = table['table']
    elif isinstance(table, list):
        # list, or inline sequence
        select = table
    elif isinstance(table, re.Match):
        # string, link to table in TABLE_GROUP
        if table.group(1) in TABLE_GROUP:
            select = TABLE_GROUP[table.group(1)]['table']
    else:
        # unknown return empty string to stop
        return ''

    # get table weights
    weight_re = r'(\d+)\*\s([\w\s\^]+)'

    weights = get_table_weights(table)

    # select random entry from table
    choice = random.choices(select, weights=weights)[0]

    # if a list has been picked, re-choose from that list
    if isinstance(choice, list):
        return choose_entry_from_table(choice)

    # remove weight from choice, if present
    if (m := re.match(weight_re, choice)):
        choice = m.group(2)

    # follow table links
    links_re = r'\^([\w\s]+)\^'

    choice = re.sub(links_re, choose_entry_from_table, choice)
 
    # replace die rolls
    dice_re = r'~(\d+)[dD](\d+)([-+*]\d+)*'
    
    choice = re.sub(dice_re, dice_roll, choice)
    
    # returned cleaned up string
    return choice.replace('_', '')


def dice_roll(die):
    # 'die' is a match object
    
    number = die.group(1)
    sides = die.group(2)
    modifier = die.group(3)
        
    total = 0
    
    for _ in range(int(number)):
        total += random.randint(1, int(sides))

    if modifier:
        value = int(modifier[1:])
        
        if modifier.startswith('+'):
            total += value
        elif modifier.startswith('-'):
            total -= value
        elif modifier.startswith('*'):
            total *= value
        
    return str(total)


def make_valid_table(table):
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
            table['show'] = False
    else:
        table['show'] = True

    if 'order' in table:
        if not isinstance(table['order'], int):
            table['order'] = 1
    else:
        table['order'] = 1

    if 'newline' in table:
        if not isinstance(table['newline'], bool):
            table['newline'] = False
    else:
        table['newline'] = True
    
    if 'heading' in table:
        if isinstance(table['heading'], bool):
            if table['heading']:
                table['heading'] = table['title']
            else:
                table['heading'] = ''
    else:
        table['heading'] = ''         
    
    if 'format' in table:
        if isinstance(table['format'], str):
            if '^' not in table['format']:
                table['format'] += ' ^'
        else:
            table['format'] = '^'    
    else:
        table['format'] = '^'
    
    if 'repeat' in table:
        if not isinstance(table['repeat'], int):
            table['repeat'] = 1
    else:
        table['repeat'] = 1

    return True


def prepare_tables(tables):
    '''convert list of tables from YAML file into TABLES dict
    '''
    
    global TABLE_GROUP
    TABLE_GROUP = {}

    for table in tables:
        if not make_valid_table(table):
            return False
        
    for table in sorted(tables, key=lambda x: x['order']):
    
        if table['title'] in TABLE_GROUP:
            print(f'error duplicate title: {table["title"]}')
            return False
        
        TABLE_GROUP[table['title']] = table

    return True
        
    
def gametables(source, target):

    # read table file
    with open(source, 'r', encoding="utf8") as s:
        tables = [t for t in yaml.safe_load_all(s)]

    if not prepare_tables(tables):
        print('Table format error')
        exit()

    t = open(target, 'w', encoding='utf8') if target else sys.stdout

    # TABLE_GROUP is a dict but keeps insertion order
    global TABLE_GROUP

    for _, table in enumerate(TABLE_GROUP):
        
        global TABLE_RECURSION_COUNT
        TABLE_RECURSION_COUNT = 0
        
        # replace with function that gathers together the output for a table
        # then can use this for linked tables...
        
        for _ in range(TABLE_GROUP[table]['repeat']):

            if not TABLE_GROUP[table]['show']:
                continue
        
            if TABLE_GROUP[table]['heading']:
                result = TABLE_GROUP[table]['heading'] + '\n'
            else:
                result = ''
                
            result += choose_entry_from_table(TABLE_GROUP[table])
        
            result = TABLE_GROUP[table]['format'].replace('^', result, 1)
        
            end = '\n' if TABLE_GROUP[table]['newline'] else ''
            
            result += end
  
            # write tidied up result
            t.write(result.strip(' '))

    if t is not sys.stdout:
        t.close()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Randomly choose an entry from a sequence in a YAML file")
    parser.add_argument("source", help="Source file (YAML)")
    args = parser.parse_args(args)

    gametables(args.source, '')


if __name__ == "__main__":
    main()
