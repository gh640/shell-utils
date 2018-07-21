'''Gathers the module docs in `.py`.
'''

import importlib
from pathlib import Path

TARGET_SUFFIXES = ('.py',)
EXCLUDED_PREFIX = '_'
TEMPLATE_ITEM = '- `{}`: {}'


def main():
    print_module_doc(x for x in get_entries_in_script_dir(is_target))


def get_entries_in_script_dir(rule):
    path = Path(__file__).resolve().parent
    return (x for x in path.iterdir() if rule(x))


def is_target(path):
    return (
        path.is_file()
        and path.suffix in TARGET_SUFFIXES
        and not path.name.startswith(EXCLUDED_PREFIX)
    )


def print_module_doc(paths):
    for path in paths:
        module = importlib.import_module(path.stem)
        print(TEMPLATE_ITEM.format(path.name, module.__doc__.strip()))


if __name__ == '__main__':
    main()
