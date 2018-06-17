'''Get Google Chrome bookmark entries
'''

import csv
import getpass
import json
import sys
from typing import Callable

config = {
    # macOS:
    'chrome_bookmark_path': (
        '/Users/{username}/Library/Application Support/'
        'Google/Chrome/Default/Bookmarks'
    ).format(username=getpass.getuser()),
}


def main():
    data = get_chrome_bookmark_data()

    # printer = Printer(RawPrintStrategy())
    # printer = Printer(SimplePrintStrategy())
    printer = Printer(CsvPrintStrategy())

    printer.walk(data)


def get_chrome_bookmark_data() -> dict:
    '''Get the json of user's Chrome bookmark.'''
    with open(config['chrome_bookmark_path']) as f:
        return json.load(f)


def walk_bookmark(entry: dict, callback: Callable) -> None:
    '''Walk through bookmark entry tree.

    Execute a callback function for bookmark entries.
    '''
    if isinstance(entry, list):
        for child in entry:
            walk_bookmark(child, callback)

    if isinstance(entry, dict):
        if 'type' in entry:
            if entry['type'] == 'folder':
                walk_bookmark(entry['children'], callback)
            elif entry['type'] == 'url':
                callback(entry)


class Printer:
    '''Base Printer class for a bookmark entry.

    Includes the following functions.
    - Prints a boomark entry.
    - Stores the count of times the method is invoked.
    '''
    def __init__(self, print_strategy):
        self.print_strategy = print_strategy
        self.count = 0

    def walk(self, data):
        walk_bookmark(data['roots']['bookmark_bar'], self.print)
        walk_bookmark(data['roots']['other'], self.print)
        print('Total: {}'.format(self.count))

    def print(self, entry) -> None:
        self.print_strategy.print(entry)
        self.count += 1


class RawPrintStrategy:
    def print(self, entry) -> None:
        print(entry)


class SimplePrintStrategy:
    def print(self, entry) -> None:
        print('{}: {}'.format(entry['name'], entry['url']))


class CsvPrintStrategy:
    def __init__(self):
        self.writer = csv.writer(sys.stdout)

    def print(self, entry) -> None:
        self.writer.writerow([
            entry['id'],
            entry['name'],
            entry['date_added'],
            entry['url'],
        ])


if __name__ == '__main__':
    main()
