# Introduction

There are a number of RPG accessories that allow a GM to build all sorts of things from groups of tables: caverns, catacombs, solar systems, galaxy sectors, names of every description... Now, while it is certainly fun to roll dice it is not always practical and can be time consuming. Hence `gametables`, a Python program that will read in a YAML file containing the specification of group of tables that will then be randomly rolled. The output is printed on the terminal or sent to a file.

## Installation

```
$ pip install --upgrade gametables
```

## Usage

The `gametables` script simply takes one or two arguments: the YAML file containing the data and optionally the output (text) file name:

```
$ python -m gametables monsters.yaml
```

Or use the console script:

```
$ gametables monsters.yaml result.txt
```


## YAML file format

Tables and table groups are stored in a [YAML 1.2 file](https://yaml.org/spec/1.2/spec.html). It must contain at least two keys: `name`, which maps to a string and acts as a reference (or ID) for the table and `table` which maps to a sequence of entries. For example, the running the file:

```
---
name: Wandering Monsters
table:
-  goblins
-  orcs
-  hobgoblins
```

will choose a random entry from the `table` section. As there are three entries there is a one in three chance of each one being output. In effect, the program is  rolling "1d3" on the table. The weighting of an entry can be adjusted by prefixing it with `N* ` where N is the increased weighting. For example:

```
---
name: Wandering Monsters
table:
-  2* goblins
-  orcs
-  hobgoblins
```

is the same as:

```
---
name: Wandering Monsters
table:
-  goblins
-  goblins
-  orcs
-  hobgoblins
```

An entry can also contain a sequence in "flow" style. For example, consider this file:

```
---
name: Wandering Monsters
table:
-  [skeletons, zombies]
-  [goblins, hobgoblins]
```

There is a fifty-fifty chance of choosing the "skeletons, zombies" line, and then a fifty-fifty chance of choosing either "skeletons" or "zombies". Flow sequences can also have weights, e.g. `[3* skeletons, zombies]`, but an entry containing a flow sequence cannot.

Multiple tables can be specified in the same file:

```
---
name: Wandering Monsters
table:
-  2* goblins
-  orcs
-  hobgoblins
...
---
name: Time of Day
table:
-  morning
-  afrternoon
-  night
```

which would produce something similar to the following:

```
orcs
night
```


### Table Specification

The full specification for a table, with all the allowable options, is as follows:

#### name

The name of the table, as a string. This is used as a heading (if the `heading` parameter is set to 'True') and to reference the table via a link (see below). Names should be unique, but this is not enforced which might lead to odd results.

#### table

A sequence of entries that will be selected from. An entry can be:

-  A string, e.g. "goblins", with an optional weighting, e.g. "3* goblins", or
-  A YAML flow sequence, e.g. "['goblins', 'orcs']". Elements of the flow sequence can have weightings as above, but the flow sequence as a whole cannot.

#### show

A boolean value determining if the output of the table is displayed. The default is 'true'; set to 'false' if the table will only be referred to via a link.

#### order

The order (an integer) in which the output from the tables should be displayed. The default order is the order in the YAML document. Specifying two tables with the same order may result in undefined results.

#### newline

A boolean value determining if the output of the table has a newline appended to it. The default is 'true'.

#### heading

This may be either a boolean value or a string; the default is 'false'. If 'true' then the 'name' field is prepended to the output, along with a newline character. If a string then that string is used as the heading. For example:

```
---
name: Wandering Monsters
heading: 'You have encountered:'
table:
-  goblins
-  orcs
-  hobgoblins
```

might result in:

```
You have encountered:
goblins
```

Note that the trailing colon means that the string must be quoted (as per the YAML specification).

### format

A string used to format the output of the table. This string should contain the `^` character, which will be replaced by the results of the "roll" on the table. The default is simply `^` (i.e. the result itself) and the string ` ^` (i.e. space and caret) will be added to the `format` if is does not contain a caret. For example:

```
---
name: Wandering Monsters
format: There are some ^ in the room
table:
-  goblins
-  orcs
-  hobgoblins
```

might produce:

```
There are some orcs in the room
```

### repeat

The number of times to roll on the table. The default is 1. This can be either an integer or a string. When the table is "rolled" this parameter is evaluated for variables (see below), and converted to an integer (defaulting to 1, if it cannot). So the following are all equivalent (see also Variables, below):

```
---
name: Wandering Monsters
repeat: 2
table:
-  goblins
-  orcs
-  hobgoblins
```

```
---
name: Wandering Monsters
repeat: $num$
vars: $num=2$
table:
-  goblins
-  orcs
-  hobgoblins
```

### vars

A string containing any number of variable assignments (see below). This parameter will be evaluated when the table is read (in fact, when *all* the tables are read) so it can be used to set up variables for use elsewhere. Note that dice rolls are evaluated *before* the variables are set so:

```
vars: $num=$1d6$$
```

will set `num` to a value between 1 and 6. 

Note that the `vars` field of each table is read and evaluated in the order they are read, so it is quite possible to overwrite variables. 

### Table Links

Table entries can contain "links" to other tables. The "linked" table is then rolled and the results replace the "link". To link to another table simply enclose the name of the table in caret characters. For example:

```
---
name: Wandering Monsters
table:
- ^Goblinoids^
- ^The Undead^
...
---
name: Goblinoids
show: false
table:
-  goblins
-  orcs
-  hobgoblins
...
---
name: The Undead
show: false
table:
-  skeletons
-  zombies
...
```

has a equal chance of "rolling" on the "Goblinoids" or "The Undead" tables. Note that linked tables typically have `show: false` to prevent repetitions. Table names (and therefore links) are case and space sensitive. Linked tables can themselves contain links, but each table can only be visited or "rolled" 20 times (to prevent infinite recursion).

Links can contain variable references, for example: `^$size$ $type$^` might refer to tables called "Large Undead", "Small Beasts" etc, depending on the value of `$size$` and `$type$`.


### Dice Expressions

Table entries can contain references to die roll expressions, of the form "$NdS+M$", where N is the number of dice, S is the number of sides and M is the modifier. Modifiers can be added, subtracted, multiplied or divided (the latter using integer arithmetic so, e.g., "1d3/3" would result in "0", "0" or "1"). These expressions are evaluated when the entry is output. For example:

```
---
name: Wandering Monsters
table:
-  $1d6+1$ goblins
-  $1d4-1$ orcs
-  $1d7$ hobgoblins
-  $2d6*2* kobolds
```

might result in:

```
4 goblins
```

Dice rolls can also appear in the `vars` field as part of a variable definition, as described above.


### Variables

Variables can be defined in the `vars` parameter, as described above. They can also be defined as part of a table entry, in which case they are set when that entry is output. 

Variables are set using the notation `$name=value$` and used using `$name$`.

For example:

```
---
name: Wandering Monsters
table:
-  goblins $num=4$
-  orcs $num=$1d2+1$$
-  hobgoblins $num=3$
...
name: Monster Type
repeat: $num$
table:
-  Warrior
-  Soldier
-  Mage
...
```

Variables are set first, removing the expression from the entry. Then all variables are resolved to their values, also removing the expression.

All variables are "global" and there is no checking for or protection from overwriting an existing variable.


## Development Notes

### Unit testing

A small number of tests are included in the `test_gametables.py` file and can be run using the [pytest](https://pypi.org/project/pytest/) application.

### Packaging a distribution

When ready for a release use the [bumpversion](https://pypi.org/project/bumpversion/) application to update the version number, e.g.

```
$ bumpversion major --tag
```

This will update the source file and the setup configuration. Then build the distribution:

```
$ python setup.py bdist_wheel
```
