'''Tests for gametables
'''

import os
import pytest

from gametables import gametables


def test_gamecards(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test
table:
-  line 1
-  line 2
''')
    
    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file is one of two lines
    expect1 = 'line 1\n'
    expect2 = 'line 2\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in [expect1, expect2]
    

def test_gamecards_single(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test
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
title: test
table:
-  ['part 1', 'part 2']
''')
    
    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file is one of two parts
    expect = ['part 1', 'part 2']


    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_inline_weighted(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test
table:
-  ['3* part 1', 'part 2']
''')
    
    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file is one of two parts
    expect = ['part 1', 'part 2']

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in expect


def test_gamecards_stdout(tmpdir, capsys):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test
newline: false
table:
-  line 1
-  line 2
''')
    
    gametables(yaml_file, '')

    # assert contents of output file is one of two lines to stdout
    expect1 = 'line 1'
    expect2 = 'line 2'

    captured = capsys.readouterr()

    assert captured.out in [expect1, expect2]


def test_gamecards_two(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test1
table:
-  line 1
...
---
title: test2
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
title: test1
order: 2
table:
-  line 1
...
---
title: test2
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
title: test1
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
title: test1
table:
-  line 1
...
---
title: test2
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


def test_gamecards_heading(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test
heading: true
table:
-  line 1
''')
    
    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has heading same as title
    expect = 'test\nline 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_heading_alt(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test
heading: foo
table:
-  line 1
''')
    
    out_file = tmpdir.join('tables.txt')

    gametables(yaml_file, out_file)

    # assert correct output files exist
    assert os.path.exists(out_file)

    # assert contents of output file has heading as supplied
    expect = 'foo\nline 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect


def test_gamecards_link(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test1
table:
-  ^test2^
...
---
title: test2
show: false
newline: false
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
title: test1
table:
-  This is ^test2^ and ^test 3^ testing
...
---
title: test2
show: false
newline: false
table:
-  line 2
...
---
title: test 3
show: false
newline: false
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


def test_gamecards_link_nested(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test1
table:
-  This is ^test2^
...
---
title: test2
show: false
newline: false
table:
-  ^test 3^
...
---
title: test 3
show: false
newline: false
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
title: test1
table:
-  This is ^test2^ and ^test2^
...
---
title: test2
show: false
newline: false
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


def test_gamecards_link_loop(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test1
table:
-  This is ^test2^
...
---
title: test2
show: false
newline: false
table:
-  ^test 3^
...
---
title: test 3
show: false
newline: false
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
title: test1
table:
-  ['^test2^', '^test3^']
...
---
title: test2
show: false
newline: false
table:
-  line 2
...
---
title: test3
show: false
newline: false
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
title: test
newline: false
table:
-  ~1d6
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
title: test
newline: false
table:
-  ~1d2 and ~1d2
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
title: test
newline: false
table:
-  ~1d6+1
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
title: test
newline: false
table:
-  ~1d6-1
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
title: test
newline: false
table:
-  ~1d3*2
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


def test_gamecards_dice_inline_list(tmpdir):

    yaml_file = tmpdir.join('tables.yaml')
    yaml_file.write(f'''---
title: test
table:
-  [~1d6, ~1d6]
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
