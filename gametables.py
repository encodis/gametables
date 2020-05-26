#!/usr/bin/env python

""" gametables.py

    Choose random entries from sequences in a YAML file
"""

import argparse
import sys
import re
import random

from dataclasses import dataclass, field
from typing import ClassVar, Any, List, Dict, Union

import yaml
from py_expression_eval import Parser


__version__ = '0.1.0'

DEFAULT_MAX_LIMIT = 20


@dataclass
class GameTable:
    '''GameTable class definition
    '''
    name: str
    table: List[Union[str, list]]
    lookup: Union[bool, str] = False
    show: bool = True
    order: int = 1
    header: str = ''
    format: str = '^\n'
    footer: str = ''
    repeat: Union[int, str] = 1
    variables: str = ''
    _weights: List[str] = field(default_factory=list)
    _min_roll: int = -1
    _visits: int = 0

    database: ClassVar[Dict[str, Any]] = {}
    variable: ClassVar[Dict[str, str]] = {}
    exparser: ClassVar[Parser] = Parser()
    maxlimit: ClassVar[int] = DEFAULT_MAX_LIMIT

    dice_re: ClassVar[str] = r'(\d+)[dD](\d+)'
    expr_re: ClassVar[str] = r'\$([\w\s()+\-*/^]*)\$'
    weight_re: ClassVar[str] = r'(\d+)\*\s(.+)'
    lookup_re: ClassVar[str] = r'(\d+)-?(\d+)?\s(.+)'
    setvar_re: ClassVar[str] = r'\$(\w+)=([\w\s()+\-*/]*)\$'
    getvar_re: ClassVar[str] = r'\$(\w+)\$'
    links_re: ClassVar[str] = r'\^([\w\s-]+)\^'

    def __post_init__(self):
        '''Check/correct properties
        '''

        if '^' not in self.format:
            self.format += ' ^'

        if self.lookup:
            table = []

            for entry in self.table:
                match = re.match(GameTable.lookup_re, entry)

                if match:
                    line = match.groups(match.group(1))
                else:
                    print(f'Bad lookup table for {self.name}')
                    sys.exit()

                if self._min_roll == -1:
                    self._min_roll = int(line[0])

                for _ in range(int(line[0]), int(line[1])+1):
                    table.append(line[2])

            self.table = table

            # if lookup was True, replace with expression based on size of table
            if isinstance(self.lookup, bool):
                self.lookup = f'$1d{len(table)}$'
            else:
                # TODO check its a valid expression using dice_re
                pass

        else:
            #  get table weights, reformat table entries without them
            self._weights = [self.get_weight(entry) for entry in self.table]
            self.table = [self.del_weight(entry) for entry in self.table]

        # evaluate dice rolls in variables
        self.variables = re.sub(GameTable.dice_re, roll_dice, self.variables)

        # set variables
        re.sub(GameTable.setvar_re, self.set_variable, self.variables)

        # add to database of all tables
        if self.name != '_' and self.name in GameTable.database:
            print(f'Duplicate table name {self.name}')

        GameTable.database[self.name] = self

    def result(self):
        '''Return results from a table, repeating the choice as required
           and adding the heading.
        '''

        if isinstance(self.repeat, str):
            try:
                repeat = int(re.sub(GameTable.expr_re, self.parse_expr, self.repeat))
            except ValueError:
                repeat = 1
        else:
            repeat = self.repeat

        result = ''

        for _ in range(repeat):
            result += self.format.replace('^', self.choose(), 1)

        if len(result) > 0:
            if self.header:
                result = self.header + result
            if self.footer:
                result = result + self.footer

        # replace 'empty string' marker
        return result.replace('__', '').lstrip(' ')

    def choose(self):
        '''Choose an item from the table, using weights, following links, and resolving
           expressions.
        '''

        # check for too deep recursion
        self._visits += 1

        if self._visits > GameTable.maxlimit:
            return ''

        # select random entry from table
        if self.lookup:
            try:
                lookup = int(re.sub(GameTable.expr_re, self.parse_expr, self.lookup))
            except ValueError:
                lookup = 1

            if lookup < self._min_roll:
                lookup = self._min_roll

            # get index from lookup
            lookup -= 1

            # constrain index, rather than raise exception
            lookup = lookup if lookup > 0 else 0
            lookup = lookup if lookup < len(self.table) - 1 else len(self.table) - 1

            choice = self.table[lookup]
        else:
            choice = random.choices(self.table, weights=self._weights)[0]

        # if a list has been picked, re-choose from that list
        if isinstance(choice, list):
            # make temp GameTable
            table = GameTable('_', choice)
            return table.choose()

        # set variables first, remove expression when done
        choice = re.sub(GameTable.setvar_re, self.set_variable, str(choice))

        # parse expression, resolve die rollss using variables
        choice = re.sub(GameTable.expr_re, self.parse_expr, choice)

        # follow table links
        for link in re.findall(GameTable.links_re, choice):
            if link in GameTable.database:
                choice = choice.replace('^' + link + '^', GameTable.database[link].result(), 1)

        # if choice can be converted to an int, do so and format with comma separators
        try:
            choice = f'{int(choice):,}'
        except ValueError:
            pass

        return choice

    @classmethod
    def sort(cls):
        '''Sort the GameTable database by order
        '''

        cls.database = {k: v for k, v in sorted(cls.database.items(), key=lambda item: item[1].order)}

    @classmethod
    def get_weight(cls, entry):
        '''Extract weight from a table entry
        '''

        if isinstance(entry, str):
            match = re.match(cls.weight_re, entry, re.DOTALL)

            if match:
                return int(match.group(1))

            return 1

        return 1

    @classmethod
    def del_weight(cls, entry):
        '''Remove weight from a table entry
        '''

        if isinstance(entry, str):
            match = re.match(cls.weight_re, entry, re.DOTALL)

            if match:
                return match.group(2)

            return entry

        return entry

    @classmethod
    def parse_expr(cls, expr):
        '''Parse an expression, including resolving die rolls
        '''
        # expr is a match object
        # first replace dice rolls in match group, return string with replacements
        expr = re.sub(GameTable.dice_re, roll_dice, expr.group(1))

        try:
            result = int(GameTable.exparser.parse(expr).evaluate(GameTable.variable))
        except ValueError:
            # expr contains unknown variable, or variable of string type
            if expr in GameTable.variable:
                result = GameTable.variable[expr]
            else:
                result = expr

        # return string for replacement
        return str(result)

    @classmethod
    def set_variable(cls, var):
        '''Set a variable
        '''

        # evaluate dice rolls, if variable contains one
        variable = re.sub(GameTable.dice_re, roll_dice, var.group(2))

        # if var can be converted to float do so, else leave as string
        try:
            variable = float(GameTable.exparser.parse(variable).evaluate(GameTable.variable))
        except:
            variable = var.group(2)

        cls.variable[var.group(1)] = variable

        # return empty string to remove expression and mark "as read"
        return ''


def roll_dice(dice):
    '''Roll a dice expression
    '''

    # dice is a match object
    number, sides = dice.groups('')

    total = 0

    for _ in range(int(number)):
        total += random.randint(1, int(sides))

    return str(total)


def gametables(source, target='', repeat=1, separator='', maxlimit=DEFAULT_MAX_LIMIT, seed=''):
    '''Output tables from source file
    '''

    if seed:
        random.seed(seed)

    with open(source, 'r', encoding='utf8') as source_file:
        try:
            raw_tables = [t for t in yaml.safe_load_all(source_file)]
        except yaml.scanner.ScannerError:
            print(f'YAML format error in {source}')
            sys.exit()

    target_file = open(target, 'w', encoding='utf8') if target else sys.stdout

    for _ in range(repeat):

        # reset database
        GameTable.database = {}

        # re-create database, so variables are correct
        for table in raw_tables:
            GameTable(table.get('name'),
                      table.get('table'),
                      table.get('lookup', False),
                      table.get('show', True),
                      table.get('order', 1),
                      table.get('header', ''),
                      table.get('format', '^\n'),
                      table.get('footer', ''),
                      table.get('repeat', 1),
                      table.get('variables', '')
                      )

        GameTable.sort()

        GameTable.maxlimit = maxlimit

        # iterate list of GameTable keys because it might change during the loop if temp tables are added
        for table in list(GameTable.database):

            if not GameTable.database[table].show:
                continue

            result = GameTable.database[table].result()

            target_file.write(result)

        # if repeating, print separator
        if repeat > 1:
            target_file.write(separator + '\n')

    if target_file is not sys.stdout:
        target_file.close()


def main(args=None):
    ''' Parse command line arguments and run
    '''

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Randomly choose an entry from a sequence in a YAML file')
    parser.add_argument('source', help='Source file (YAML)')
    parser.add_argument('--target', nargs='?', default='', help='Target file (text)')
    parser.add_argument('-r', '--repeat', type=int, default=1, help='Repeat run')
    parser.add_argument('-s', '--separator', type=str, default='', help='Repeat separator')
    parser.add_argument('-m', '--maxlimit', type=int, default=DEFAULT_MAX_LIMIT, help='Max recursion limit per table')
    parser.add_argument('--seed', type=str, default='', help='Seed for random number generator')
    args = parser.parse_args(args)

    gametables(args.source,
               target=args.target,
               repeat=args.repeat,
               separator=args.separator,
               maxlimit=args.maxlimit,
               seed=args.seed)


if __name__ == "__main__":
    main()
