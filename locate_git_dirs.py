'''Finds git-enabled directories in a path.
'''


import argparse
from pathlib import Path
import subprocess
from contextlib import contextmanager


def main():
    args = get_args()
    directory = args.directory
    locate_git_dirs(directory)


def get_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('directory', type=dir_factory)
    return parser.parse_args()


def dir_factory(path_str: str):
    path = Path(path_str)
    if not path.is_dir():
        message = "Invalid directory: '{}'".format(path_str)
        raise argparse.ArgumentTypeError(message)
    return path


def locate_git_dirs(parent: Path):
    for entry in parent.iterdir():
        if not entry.is_dir():
            continue
        result = subprocess.run(
            ['git', 'status'],
            cwd=entry,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            print('{}'.format(entry))


if __name__ == '__main__':
    main()
