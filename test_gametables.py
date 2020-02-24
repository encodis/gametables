'''Tests for gametables
'''

import os

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

    # assert contents of output file is one of two lines
    expect1 = 'part 1'
    expect2 = 'part 2'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual in [expect1, expect2]


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

    # assert contents of output file is one of two lines
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

    # assert contents of output file same as input
    expect = 'line 1\nline 2\n'

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

    # assert contents of output file same as input
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

    # assert contents of output file same as input
    expect = 'foo\nline 1\n'

    with open(out_file, 'r', encoding='utf8') as fh:
        actual = fh.read()

    assert actual == expect
