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

An alternative is to use lookup tables, which will be what are printed in most RPGs. Use the `lookup` parameter, with a value or expression to "roll" and include the ranges on each line. For example:

```
---
name: Wandering Monsters
lookup: $1d4$
table:
-  1-2 goblins
-  3 orcs
-  4 hobgoblins
```


Multiple tables can be specified in the same file:

```
---
name: Wandering Monsters
format: '^'
table:
-  2* goblins
-  orcs
-  hobgoblins
...
---
name: Time of Day
table:
-  morning
-  afternoon
-  night
```

which would produce something similar to the following:

```
orcs night
```

> NOTE: entries can be quoted to include tabs etc but use double quotes XXX

### Table Specification

The full specification for a table, with all the allowable options, is as follows:

#### name

The name of the table, as a string. This is used as a heading (if the `heading` parameter is set to 'True') and to reference the table via a link (see below). Names should be unique, but this is not enforced which might lead to odd results.

#### table

A sequence of entries that will be selected from. An entry can be:

-  A string, e.g. "goblins", with an optional weighting, e.g. "3* goblins", or
-  A YAML flow sequence, e.g. "['goblins', 'orcs']". Elements of the flow sequence can have weightings as above, but the flow sequence as a whole cannot.
-  It is tricky to have a blank line as an entry in a table. The double underscore "__" sequence will be removed from any entry to facilitate this.

#### lookup

Instructs the program to treat the table as a lookup table. The ranges must be supplied for each line in `A-B` format, although if this is not supplied then a "1" is assumed. The default value is `false`. If `true` then the dice roll used for the lookup will be calculated from the number of entries in the table, i.e. five entries will lead to a "1d5". (However, this will ignore any ranges that have been given).

However, most of the time `lookup` field will be an expression, e.g. `$2d6$`. Variables can also be included (provided they have been set beforehand), e.g. `$2d6 + terrain_mod$`

#### format

A string used to format the output of the table. This string should contain the `^` character, which will be replaced by the results of the "roll" on the table. The default is simply `^\n` (i.e. the result itself, followed by a newline) and the string ` ^` (i.e. space and caret) will be added to the `format` if is does not contain a caret. For example:

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

Format strings can contain control characters like tab and newline, but make sure the string is double quoted, e.g. `format: "\tNumber: ^ \n"`. To prevent the table adding a newline replace the default format with the caret character only, i.e. `"^"`.

#### show

A boolean value determining if the output of the table is displayed. The default is 'true'; set to 'false' if the table will only be referred to via a link.

#### order

The order (an integer) in which the output from the tables should be displayed. The default order is the order in the YAML document. Specifying two tables with the same order may result in undefined results.

#### header

A string that is prepended to the output of the entire table (i.e. after all the `repeat`s). As with the `format` field this will need to be quoted if it contains control characters. For example:

```
---
name: Wandering Monsters
header: "You have encountered:\n"
format: "    ^\n"
repeat: 2
table:
-  goblins
-  orcs
-  hobgoblins
```

should result in something similar to:

```
You have encountered:
    goblins
    orcs
```

Note that the trailing colon also means that the string must be quoted (as per the YAML specification). Also note that the header will not be printed if the result of the table is empty (i.e. a zero length string).

#### footer

A string that is appended to the output of the entire table (i.e. after all the `repeat`s). 

#### repeat

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

#### vars

A string containing any number of variable assignments (see below). This parameter will be evaluated when the table is read (in fact, when *all* the tables are read) so it can be used to set up variables for use elsewhere. Note that dice rolls are evaluated *before* the variables are set so:

```
vars: $num=1d6$
```

will set `num` to a value between 1 and 6. 

Note that the `vars` field of each table is read and evaluated in the order they are read, so it is quite possible to overwrite variables. This field is useful when using modifiers to lookup rolls, as it can be used to set default values.

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

has a equal chance of "rolling" on the "Goblinoids" or "The Undead" tables. Note that linked tables typically have `show: false` to prevent that table being printed out and the output repeated. Table names (and therefore links) are case and space sensitive. Linked tables can themselves contain links, but each table can only be visited or "rolled" 20 times (to prevent infinite recursion).

Links can contain variable references, for example: `^$size$ $type$^` might refer to tables called "Large Undead", "Small Beasts" etc, depending on the value of `$size$` and `$type$`.


### Expressions

Table entries can contain simple arithmetic expressions. Variables that have been set will be used in these expressions (but recall that the order in which the tables are "rolled" is important). Any strings of the form `XdY` will be replaced by the appropriate dice roll (with X as the number of dice and Y the number of sides). This makes it possible to construct tables like this:

```
---
name: Wandering Monsters
vars: $danger=1d4$
table:
-  $1d6+1+danger$ goblins
-  $1d4-1+danger$ orcs
-  $1d7+danger$ hobgoblins
-  $(2d6*2)+danger-1d4$ kobolds
```

Dice rolls can also appear in the `vars` field as part of a variable definition, as well as the `lookup` field.


### Variables

Variables can be defined in the `vars` parameter, as described above. They can also be defined as part of a table entry, in which case they are set when that entry is output. 

Variables are set using the notation `$name=value$`. They are used simply using the name in an expression.

Variables can evaluate to either strings or integers: if a variable (or, for that matter, the result of an expression) can be converted to an integer it will be. Otherwise it will be a string. This means that if, say, the variable `num` is not defined when the expression `$1d4 + num$` is evaluated the result will be the string `1d4 + num`. Integer variables are also formatted using comma separators.

For example:

```
---
name: Wandering Monsters
table:
-  goblins $num=4$
-  orcs $num=1d2+1$
-  hobgoblins $num=3$
...
---
name: Monster Type
repeat: $num$
table:
-  Warrior
-  Soldier
-  Mage
...
```

Variables are set first, removing the expression from the entry. Then all expressions are evaluated with the result replacing the expression in the entry. Note that variables are defined in the order they are encountered when outputting the tables: if a table has `show: false` then any variables it defines will not be set unless some other table runs it via a table link.

All variables are "global" and there is no checking for or protection from overwriting an existing variable.

## Example Files

The **examples** folder in the repo contain some annotated examples of input YAML file. The first is the "Adventure Title" generator from Modiphious' Gamemasters Toolkit (**conan_adv_titles.yaml**). Some sample results are quite good:

```
Shadow in the Pool
A/an Empress Is/Will Be/Shall Be Cursed
The Iron Gem of the Skull
A/An Storm of Shadow
```

Others might need some work:

```
Bone
The Lost of Queen
Fallen of Specter
```

although "Bone" is not a bad name for a Conan adventure!

Another example is from "Catacombs of Hyboria", Second Edition by Mongoose Publishing (**conan_catacombs.yaml**). This is a much more complex generator with numerous tables (some of them two dimensional) and various modifiers. Some sample output is:

```
Type:   Hollow  
Size:   Average 
Area:   400 sq. ft.
Depth:  85 ft.
Terrain:
        Man-Made:    Burial Chamber (decrepit, 50% chance of treasure worth 1200 silver pieces)
```

and 

```
Type:   Cavern System  
Size:   Average 
Area:   1,800,000 sq. ft.
Depth:  2,550 ft.
Terrain:
        Flora:       Common Growth (area 50%)
        Surface:     Gorge/Cliff (span 60 ft., depth 30 ft.)
        Surface:     Pitted Stone (area 40%)
        Vast Depth:  Ancient Art/Symbols (area 40 sq. ft.)
        Surface:     Stalagmite Field (area 300 sq. ft., average height 18 in.)
        Fauna:       Crawling (insect, 100, waste is prodigious and slick)
        Fauna:       Aerial (gliding mammal, pop. 10,000, has perfect sonar and blind sight)
        Fauna:       Burrowing (mammal, pop. 1,500, naturally venomous and predatory)
        Fauna:       Burrowing (mammal, pop. 500, possesses dangerous self-defence toxins in its flesh)
        Fauna:       Large Creature (reptile, pop. 60, advanced intelligence with problem-solving)
        Surface:     Stalagmite Field (area 450 sq. ft., average height 2 ft.)
        Fauna:       Aerial (lacewing, pop. 6,000, small sized, fast)
        Ceiling:     Optical Illusion of Height
        Vast Depth:  Phosphorescent Growths (area 50%)
        Ceiling:     Optical Illusion of Height
        Vast Depth:  Abyssal Crevasse (width 100 ft.)
        Fauna:       Subterranean (worm, pop. 40, found below 100 ft., has a secondary trait)
        Surface:     Waterway Access (underground river, depth 30 ft.)
        Vast Depth:  Abyssal Crevasse (width 160 ft.)
        Surface:     Stalagmite Field (area 200 sq. ft., average height 1 ft.)
        Unique:      Lair of the Dead

Plots:
        Unearthed Graves
```

Note that the order of the terrain elements is not sorted. It would be nice if this was an option but one could consider this the order in which the elements are encountered. Also note that full descriptions of elements have not been included, so if you want to know what "Pitted Stone" and "Lair of the Dead" refer to you will need to source the book.

Another example is from the "Star Wars Roleplaying Game: Revised, Expanded, Updated" by Womp Rat Press. This is an expansion of "Star Wars: The Role Playing Game" by West End Games. The file **star_wars_planets.yaml** contains the world creator in the REUP version. Sample planets generated are: 

```
Star Wars Planet

Function:     Military  
Government:   Organized Crime
Planet Type:  Terrestrial
Terrain:      Volcanic  
Temperature:  Temperate
Gravity:      Heavy 
Atmosphere:   Type I (breathable)
Hydrosphere:  Moist
Day Length:   15 standard hours
Year Length:  465 local days
Starport:     Imperial/Republic class
Population:   5,000
Tech Level:   Hyperspace
```

and

```
Star Wars Planet

Function:     Homeworld
Government:   Dictatorship
Planet Type:  Terrestrial
Terrain:      Special
Temperature:  Temperate
Gravity:      Standard
Atmosphere:   Type I (breathable)
Hydrosphere:  Saturated
Day Length:   25 standard hours
Year Length:  345 local days
Starport:     Stellar class
Population:   82,000,000,000
Tech Level:   Hyperspace
```

Note that the one thing not included here are the "Incompatible Conditions", such as not having an Agricultural planet in an Asteroid Belt.

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

## To Do

- Catch more YAML and expression parser exceptions
- Warn of unknown YAML fields
- Warning of duplicate table names
- Option line option to roll multiple times, with separators (-r, --repeat, --separator)
- Option to report RNG seed, and to use it to replicate a table (--seed, --seed=XXX)
- Option to dump YAML file in Markdown format (--dump)
- Option for changing recursion limit (--max-recursion)
- Option to toggle integer formatting (--integer)
- Options for tables to run without output (so variables will be set etc)
- Read a folder of YAML files (would have to define order)
- Read a zip file of YAML files
- Overall headers and footers (possible as template files)
- Warning of overwriting existing variables
- For lookup tables, check ranges are consistent
- Functionality to set up a library of files, then roll a table by name (not file itself)
- More formatting options, ideally for input to something like Pandoc
