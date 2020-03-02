#!/usr/bin/env python

""" gametables.py

    Randomly choose an entry from a sequence in a YAML file
"""

import argparse
import sys
import re
import random
import math

from dataclasses import dataclass, field
from typing import ClassVar, Any, List, Dict, Union

import yaml


__version__ = '0.0.1'


@dataclass
class GameTable:
    name: str
    table: List[Union[str, list]]
    show: bool = True
    order: int = 1
    newline: bool = True
    heading: Union[bool, str] = False
    format: str = '^'
    repeat: Union[int, str] = 1
    vars: str = ''
    _weights: List[str] = field(default_factory=list)
    _visits: int = 0

    database: ClassVar[Dict[str, Any]] = {}
    variable: ClassVar[Dict[str, str]] = {}

    dice_re: ClassVar[str] = r'\$(\d+)[dD](\d+)([-+*]\d+)*\$'
    weight_re: ClassVar[str] = r'(\d+)\*\s(.+)'
    setvar_re: ClassVar[str] = r'\$(\w+)=(\w+)\$'
    getvar_re: ClassVar[str] = r'\$(\w+)\$'
    links_re: ClassVar[str] = r'\^([\w\s]+)\^'

    def __post_init__(self):
        if isinstance(self.heading, bool) and self.heading:
            self.heading = self.name

        if '^' not in self.format:
            self.format += ' ^'

        self._weights = [self.get_weight(entry) for entry in self.table]
        self.table = [self.del_weight(entry) for entry in self.table]

        # set variables, if any, evaluating dice rolls first
        self.vars = re.sub(GameTable.dice_re, roll_dice, self.vars)

        re.sub(GameTable.setvar_re, self.set_variable, self.vars)

        # add to database of all tables
        GameTable.database[self.name] = self

    def result(self):
        '''Return result from a table
        '''

        if isinstance(self.repeat, str):
            repeat = int(re.sub(GameTable.getvar_re, self.get_variable, self.repeat))
        else:
            repeat = self.repeat

        result = ''

        for _ in range(repeat):
            result += self.format.replace('^', self.choose(), 1)
            result += '\n' if self.newline else ''

        if self.heading:
            result = self.heading + '\n' + result

        return result.strip(' ')

    def choose(self):
        '''Choose an item from the table, using weights, follow links, resolve vars/dice etc
        '''

        # check for too deep recursion
        self._visits += 1

        if self._visits > 20:
            return ''

        # select random entry from table
        choice = random.choices(self.table, weights=self._weights)[0]

        # if a list has been picked, re-choose from that list
        if isinstance(choice, list):
            # make temp GameTable
            table = GameTable('_', choice)
            return table.choose()

        # replace die rolls
        choice = re.sub(GameTable.dice_re, roll_dice, choice)

        # set vars, remove expression
        choice = re.sub(GameTable.setvar_re, self.set_variable, choice)

        # get a variable if set, and remove
        choice = re.sub(GameTable.getvar_re, self.get_variable, choice)

        # follow table links
        for link in re.findall(GameTable.links_re, choice):
            if link in GameTable.database:
                choice = choice.replace('^' + link + '^', GameTable.database[link].result(), 1)

        # returned cleaned up string
        return choice.replace('_', '')

    @classmethod
    def sort(cls):
        cls.database = {k: v for k, v in sorted(cls.database.items(), key=lambda item: item[1].order)}

    @classmethod
    def get_weight(cls, entry):
        '''extract weight from a table entry
        '''
        if isinstance(entry, str):
            if m := re.match(cls.weight_re, entry):
                return int(m.group(1))
            else:
                return 1
        else:
            return 1

    @classmethod
    def del_weight(cls,  entry):
        '''remove weight from a table entry
        '''
        if isinstance(entry, str):
            if m := re.match(cls.weight_re, entry):
                return m.group(2)
            else:
                return entry
        else:
            return entry

    @classmethod
    def set_variable(cls, var):
        '''set a variable
        '''
        # var is match object
        cls.variable[var.group(1)] = var.group(2)

        # return empty string
        return ''

    @classmethod
    def get_variable(cls, var):
        '''get a variable, return empty string if not found
        '''
        # var is match object

        return cls.variable.get(var.group(1), '')


def roll_dice(dice):
    '''roll a dice expression
    '''

    number, sides, modifier = dice.groups('')

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
        elif modifier.startswith('/'):
            total = math.trunc(total/value)

    return str(total)


def gametables(source, target):

    GameTable.database = {}

    with open(source, 'r', encoding="utf8") as s:
        for t in yaml.safe_load_all(s):
            GameTable(t.get('name'),
                      t.get('table'),
                      t.get('show', True),
                      t.get('order', 1),
                      t.get('newline', True),
                      t.get('heading', False),
                      t.get('format', '^'),
                      t.get('repeat', 1),
                      t.get('vars', '')
                      )

    GameTable.sort()

    t = open(target, 'w', encoding='utf8') if target else sys.stdout

    # make list of GameTable keys because it might change during the loop
    for table in list(GameTable.database):
        if not GameTable.database[table].show:
            continue

        result = GameTable.database[table].result()

        t.write(result)

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
