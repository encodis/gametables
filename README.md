# Introduction

There are a number of RPG accessories that allow a GM to build all sorts of things from groups of tables: caverns, catacombs, solar systems, galaxy sectors, names of every description... Now, while it is certainly fun to roll dice it is not always practical and can be time consuming. Hence `gametables`, a Python program that will read in a YAML file containing the specification of group of tables that will be randomly rolled. The output is printed on the command line or sent to a file.

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

Tables and table groups are stored in a [YAML 1.2 file](https://yaml.org/spec/1.2/spec.html). It must contain at least two keys: 'title', which maps to a string and acts as a reference for the table and 'table' which maps to a sequence of entries. For example:

```
---
title: Wandering Monsters
table:
-  goblins
-  orcs
-  hobgoblins
```

will 'roll' on the 'tables' section. As there are three entries there is a one in three chance of each one being output. The weighting of an entry can be adjusted by prefixing it with `N* ` where N is the increased weighting. For example:

```
---
title: Wandering Monsters
table:
-  2* goblins
-  orcs
-  hobgoblins
```

is the same as:

```
---
title: Wandering Monsters
table:
-  goblins
-  goblins
-  orcs
-  hobgoblins
```

An entry can also contain a sequence in "flow" style. For example, consider this file:

```
---
title: Wandering Monsters
table:
-  [skeletons, zombies]
-  [goblins, hobgoblins]
```

There is a fifty-fifty chance of choosing the "skeletons, zombies" line, and a fifty-fifty chance of choosing either "skeletons" or "zombies". Flow sequences can also have weights, e.g. `[3* skeletons, zombies]`.

## TODO

-  parse for "1d6+1" etc and roll that 
- if you had dataclasses you could make them up on the fly from an inline sequence!!!!

if you could have a metadata "variable: foo=5' in one table then
'repeat: $foo$' in another?

or even 

table:
-  This is line 1 $foo=3$
-  This is line 2 $foo=4$

.
.
.

---
repeat: $foo$
table:

when retrieving results, check for variable pattern, allocate to dict and remove
when prepping tables, allow pattern as well as str/int etc
when about to do anything with a table make a COPY, replace the var, do it

also: have a variables metadata entry that can be used explicitly - need this if table has show=false

maybe replace dice with $1d6$? or links?  if $xxx$ does not resolve to a dice roll, or a link (table title), or a variable then blank

if you did random first could have $foo=$1d6+1$$ or if links were also last ^table_$foo$^

vars with dice roll on the 'variables' metadata will be evaluated at load time - but that might not matter

or a field that says "set this variable to the result of the table"...

can replace in heading and repeat too, but repeat should be an int. maybe format too, but only vars and dice, not links


## Full table specification

```
---
title: the title of the table, used as ID
format: prefix ^ suffix  # wrap 'foo {} bar' in here, if a single word output an HTML div with this class
template: a template file or string? multiline?
heading: true|false|str    # print out title as heading, or use str as heading
show: true|false     # if false then table can be referenced but will not be printed, only applies at top level
order: 1             # order tables will be printed out, default is order in file
newline: true|false  # output newline after printing, default is true could also be number of newlines, 0, 1, 2 etc
repeat: number of time to repeat this table - might be 1d6 etc. ??? need to populate X zone, for example
table:   # if only 1 thing in table acts as a line, e.g. other text
-  goblins
-  goblins
-  orcs
-  hobgoblins
-  ^dangerous^       # insert result from table 'dangerous' in this entry if chosen
-  also ^dangerous^ here # in middle of
-  ~1d6+1 skeletons   # roll 1d6+1 and insert, match X[dD]N[+-]Y, no spaces
```


## Development notes

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
