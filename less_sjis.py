'''Read a file encoded with SJIS.
'''


import argparse
import subprocess
import sys
import tempfile
import unittest


def main():
    args = parse_args()
    text = read_sjis_file(args.file.name)
    run_less(text)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType())
    return parser.parse_args()


def read_sjis_file(path):
    with open(path, encoding='sjis') as f:
        return f.read()


def run_less(text):
    subprocess.run(['less'], input=text, encoding=sys.stdout.encoding)


class Test_read_sjis_file(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile()

    def tearDown(self):
        # No need to explicitly delete the file as it's automatically deleted.
        pass

    def test_read_sjis_file_ascii(self):
        self.temp.write('This is written with sjis.'.encode('sjis'))
        self.temp.flush()
        text = read_sjis_file(self.temp.name)
        self.assertEqual(text, 'This is written with sjis.')

    def test_read_sjis_file_non_ascii(self):
        self.temp.write('これは SJIS で書かれています。'.encode('sjis'))
        self.temp.flush()
        text = read_sjis_file(self.temp.name)
        self.assertEqual(text, 'これは SJIS で書かれています。')


if __name__ == '__main__':
    main()
