'''Tests for gametables
'''

import os
import pytest

from gametables import gametables


def test_gamecards(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
table:
-  3* line 1
-  line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file is one of two lines
    expect = ['line 1\n', 'line 2\n']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_single(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
table:
-  line 1
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file same as input
    expect = 'line 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_inline(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
table:
-  ['part 1', 'part 2']
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file is one of two parts
    expect = ['part 1\n', 'part 2\n']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_inline_weighted(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
table:
-  ['3* part 1', 'part 2']
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file is one of two parts
    expect = ['part 1\n', 'part 2\n']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_stdout(tmpdir, capsys):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  line 1
-  line 2
''')

    gametables(yaml_file, '')

    # assert contents of output file is one of two lines to stdout
    expect = ['line 1', 'line 2']

    captured = capsys.readouterr()

    assert captured.out in expect


def test_gamecards_two(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  line 1
...
---
name: test2
table:
-  line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has two lines
    expect = 'line 1\nline 2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_order(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
order: 2
table:
-  line 1
...
---
name: test2
order: 1
table:
-  line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has two lines
    expect = 'line 2\nline 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_repeat(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
repeat: 2
table:
-  line 1
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has two lines
    expect = 'line 1\nline 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_hide_one(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  line 1
...
---
name: test2
show: false
table:
-  line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has output from one table only
    expect = 'line 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_header(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
header: "a test\\n"
table:
-  line 1
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has heading same as title
    expect = 'a test\nline 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_footer(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
footer: "\\ndone!"
table:
-  line 1
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has heading same as title
    expect = 'line 1\n\ndone!'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_format_default(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: foo
table:
-  line 1
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has default format
    expect = 'foo line 1'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_lookup(tmpdir):
    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
lookup: $1d6$
table:
-  1 first
-  2-4 second
-  5-6 third
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has specified format
    expect = ['first\n', 'second\n', 'third\n']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_lookup_auto(tmpdir):
    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
lookup: true
table:
-  1 first
-  2-4 second
-  5-6 third
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has specified format
    expect = ['first\n', 'second\n', 'third\n']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_lookup_2d6(tmpdir):
    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
lookup: $2d6$
table:
-  2-7 first
-  8-11 second
-  12 third
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has specified format
    expect = ['first\n', 'second\n', 'third\n']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_lookup_fixed(tmpdir):
    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test0
format: '^'
table:
-  Line 1^test1^
...
---
name: test1
show: false
table:
-  $val=2$
...
---
name: test2
format: '^'
lookup: $val$
table:
- 1 Line 1
- 2 Line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has specified format
    expect = 'Line 1\nLine 2'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_format(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: "foo ^ bar\\n"
table:
-  line 1
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has specified format
    expect = 'foo line 1 bar\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_link(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  ^test2^
...
---
name: test2
show: false
format: '^'
table:
-  line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has line from linked table
    expect = 'line 2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_link_two(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  This is ^test2^ and ^test 3^ testing
...
---
name: test2
show: false
format: '^'
table:
-  line 2
...
---
name: test 3
show: false
format: '^'
table:
-  line 3
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has contents from two linked tables
    expect = 'This is line 2 and line 3 testing\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_link_weighted(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
format: '^'
table:
- 2* ^test2^
- 2* ^test 3^
...
---
name: test2
show: false
format: '^'
table:
-  line 2
...
---
name: test 3
show: false
format: '^'
table:
-  line 3
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has contents from two linked tables
    expect = ['line 2', 'line 3']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_link_nested(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  This is ^test2^
...
---
name: test2
show: false
format: '^'
table:
-  ^test 3^
...
---
name: test 3
show: false
format: '^'
table:
-  line 3
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has line from linked table, supplied by other linked table
    expect = 'This is line 3\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


@pytest.mark.skip(reason='Need to work out a way to test this properly')
def test_gamecards_link_no_repeat(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  This is ^test2^ and ^test2^
...
---
name: test2
show: false
format: '^'
table:
-  line 1
-  line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file are different despite referenced from same table
    expect = 'This is line 1 and line2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_link_inline_repeat(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
format: '^'
table:
-  ^test2^
...
---
name: test2
show: false
repeat: 2
table:
-  line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has contents from two linked tables
    expect = 'line 2\nline 2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_link_loop(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  This is ^test2^
...
---
name: test2
show: false
format: '^'
table:
-  ^test 3^
...
---
name: test 3
show: false
format: '^'
table:
-  ^test2^
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file are cut off due to recursion limit
    expect = 'This is \n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_link_inline(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
format: '^'
table:
-  ['^test2^', '^test3^']
...
---
name: test2
show: false
format: '^'
table:
-  line 2
...
---
name: test3
show: false
format: '^'
table:
-  line 3
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file is one of two parts
    expect = ['line 2', 'line 3']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  $1d6$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = '123456'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice_multiple(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  $1d2$ and $1d2$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice with multiple ref on line
    expect = ['1 and 1', '1 and 2', '2 and 1', '2 and 2']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice_plus(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  $1d6+1$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = '234567'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice_minus(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  $1d6-1$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = '012345'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice_multiply(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  $1d3*2$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = '246'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice_divide(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  $1d3/3$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = '01'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice_complex(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
vars: $num=2$
table:
-  $1d3+num-1$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = '234'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_dice_inline_list(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test
format: '^'
table:
-  [$1d6$, $1d6$]
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice with multiple ref on line
    expect = '123456'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_vars(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
format: '^'
table:
-  $foo=1$ Line ^test2^
...
---
name: test2
format: '^'
show: false
table:
-  Foo = $foo$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = 'Line Foo = 1'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_vars_metadata(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
show: false
vars: $foo=1$ $bar=2$
table:
-  N/A
...
---
name: test2
format: '^'
table:
-  Foo = $foo$, Bar = $bar$
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = 'Foo = 1, Bar = 2'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_vars_repeat(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
table:
-  Line 1 $foo=2$
...
---
name: test2
repeat: $foo$
table:
-  Line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = 'Line 1 \nLine 2\nLine 2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_vars_link(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
vars: $foo=2$
table:
-  Line 1 ^test$foo$^
...
---
name: test2
show: false
format: '^'
table:
-  Line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = 'Line 1 Line 2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_vars_link_str(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test1
vars: $foo_1=bar_4$
table:
-  Line 1 ^test_$foo_1$^
...
---
name: test_bar_4
show: false
format: '^'
table:
-  Line 2
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = 'Line 1 Line 2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_vars_dice(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
name: test0
vars: $foo=1d3$
format: '^'
table:
-  ^test$foo$^
...
---
name: test1
format: '^'
show: false
table:
-  Line 1
...
---
name: test2
format: '^'
show: false
table:
-  Line 2
...
---
name: test3
format: '^'
show: false
table:
-  Line 3
''')

    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file in range of dice
    expect = ['Line 1', 'Line 2', 'Line 3']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect
