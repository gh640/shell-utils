'''指定されたディレクトリの直下の空のディレクトリを全件削除する
'''

import argparse
from pathlib import Path


def main():
    '''Main function.'''
    args = get_args()
    path, is_dry_run = Path(args.path), args.is_dry_run

    print('Searching empty directories in `{}`...'.format(str(path.resolve())))
    directories = find_empty_dirs(path)

    if is_dry_run:
        print('Found:')
        print('\n'.join(str(d) for d in directories))
    else:
        print('Deleted:')
        remove_dirs(directories)


def get_args():
    '''Get command line arguments.'''
    parser = argparse.ArgumentParser('Remove empty directories.')
    parser.add_argument('path', help='Path to search files.')
    parser.add_argument('-d', '--dry-run', dest='is_dry_run', action='store_true', help='Dry run setting.')

    args = parser.parse_args()

    return args


def find_empty_dirs(parent: Path) -> list:
    '''Find empty directory under the specified directory.'''
    return [
        entry
        for entry in parent.iterdir()
        if entry.is_dir() and not len(list(entry.iterdir()))
    ]


def remove_dirs(directories: list) -> None:
    '''Remove directories.'''
    for entry in directories:
        entry.rmdir()
        print('{}'.format(entry))


if __name__ == '__main__':
    main()
