'''Gather class/interface/trait declarations in php files.
'''

import glob
from pathlib import Path
import re


FILE_PATTERN = '**/*.php'
DECLARATION_PATTERN = '(interface|class|abstract class|trait)'


def main():
    for file in iter_php_file():
        find_declaration(file, DECLARATION_PATTERN)


def iter_php_file():
    yield from glob.iglob(FILE_PATTERN, recursive=True)


def find_declaration(path, pattern):
    option = re.IGNORECASE
    re_pattern = re.compile(r'\s*' + pattern + r'\s+(?P<name>\S+)', option)
    with open(path) as f:
        for line in f:
            match = re_pattern.match(line)
            if match:
                print(match.group('name'))


if __name__ == '__main__':
    main()
