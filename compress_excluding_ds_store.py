# coding: utf-8

"""Compresses a directory into a zip file excluding .DS_Store files in MacOS.
"""


import argparse
import zipfile
from pathlib import Path
from typing import Iterable, List, Generator


settings = {'zip_extension': '.zip', 'verbose': False}


def main():
    """Main function."""
    parser = build_parser()

    args = parser.parse_args()
    skipped_names = args.skipped_names
    directory = args.directory
    settings['verbose'] = args.verbose

    zip_file = make_zip_path(directory)

    try:
        compress_dir(zip_file, directory, skipped_names)
    except CompressionError as e:
        parser.error('{}'.format(e))

    template = 'Zip file "{}" has been created (excluded names: "{}").'
    print(template.format(zip_file, ','.join(skipped_names)))


def build_parser() -> argparse.ArgumentParser:
    """Builds the command line parser."""
    parser = argparse.ArgumentParser('Compress a directory excluding .DS_Store.')
    parser.add_argument(
        '--skipped-names',
        type=skipped_names_type,
        default='.DS_Store',
        help='Skipped names.',
    )
    parser.add_argument(
        '--verbose', action='store_true', help='Make the output verbose.'
    )
    parser.add_argument('directory', type=directory_type, help='Target directory.')

    return parser


def directory_type(directory_path: str) -> Path:
    """Processes an argument for "directory" type."""
    try:
        path = Path(directory_path)
    except TypeError as e:
        message = 'Specified path is incorrect: "{}".'.format(directory_path)
        raise argparse.ArgumentTypeError(message)

    if not path.is_dir():
        message = 'Specified directory not found: "{}".'.format(path)
        raise argparse.ArgumentTypeError(message)

    return path


def skipped_names_type(names: str) -> List[str]:
    """Processes an argument for "skipped names" type."""
    return names.split(',')


def make_zip_path(directory: Path) -> Path:
    """Generates a zip path from the target directory."""
    return directory.with_suffix(settings['zip_extension'])


def compress_dir(zip_out: Path, directory: Path, skipped_names: Iterable[str]):
    """Compresses a directory into a zip file.
    """
    if zip_out.exists():
        message = 'Specified zip file already exists: "{}".'.format(zip_out)
        raise CompressionError(message)

    with zipfile.ZipFile(str(zip_out.absolute()), 'w') as z:
        if settings['verbose']:
            print('Zip file has been initialized: "{}".'.format(z.filename))
        for f in iter_all_files(directory):
            if f.name in skipped_names:
                if settings['verbose']:
                    print('Skipped: "{}".'.format(f))
                continue

            z.write(f, f.relative_to(directory))
            if settings['verbose']:
                print('Added: "{}".'.format(f))


def iter_all_files(directory: Path) -> Generator[Path]:
    """Aggregates the file paths in a directory recursively."""
    if not directory.is_dir():
        message = 'Specified directory is not found: "{}".'.format(directory)
        raise CompressionError(message)

    return directory.glob('**/*.*')


class CompressionError(Exception):
    """A custom error type for the compression process."""

    pass


if __name__ == '__main__':
    main()
