#!/usr/bin/env python3
'''Git: Commits multiple files in separate commits.
'''

from pathlib import Path
import subprocess

IS_DRY_RUN = False
FILES = '''
./data/data1.tsv
./data/data2.tsv
./data/data3.tsv
'''
MSG_TEMPLATE = '"Issue #999: Add `{}` to ..."'


def main():
    for f in (Path(x) for x in FILES.split() if x.strip()):
        git_add(f)
        git_commit(MSG_TEMPLATE, [f])


def git_add(path):
    run(['git', 'add', str(path)])


def git_commit(template, msg_args):
    msg = template.format(*msg_args)
    run(['git', 'commit', '-m', msg])


def run(args):
    if IS_DRY_RUN:
        print(' '.join(args))
    else:
        # Stop if the command has failed.
        result = subprocess.run(args, stdout=subprocess.PIPE, check=True)
        print(result.stdout.decode('utf-8'))


if __name__ == '__main__':
    main()
