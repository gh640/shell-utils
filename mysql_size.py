'''Gets MySQL databases/tables sizes.
'''

import argparse
import getpass
import subprocess
import unittest
from unittest import mock


def main():
    parser = get_parser()
    args = parser.parse_args()
    socket, user, database = args.socket, args.user, args.database

    client = Client()
    if socket:
        client.set_socket(socket)
    else:
        client.set_user(user)

    try:
        if database:
            client.check_table_sizes(database)
        else:
            client.check_database_sizes()
    except ClientException as e:
        parser.error(e)


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket', '-S', nargs='?')
    parser.add_argument('--user', '-u', nargs='?', default=getpass.getuser())
    parser.add_argument('database', nargs='?')
    return parser


def is_valid_database_param(database_name):
    '''Validates a database name to prevent SQL injection.'''
    for char in ('"', "'", ';'):
        if char in database_name:
            return False
    return True


class Client:
    def __init__(self):
        self.socket = None
        self.user = None

    def set_socket(self, socket):
        self.socket = socket

    def set_user(self, user):
        self.user = user

    def check_database_sizes(self):
        sql = '''
        SELECT table_schema AS "Database",
            ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS "Size (MB)"
            FROM information_schema.TABLES
            GROUP BY table_schema;
        '''
        self.run_query(sql)

    def check_table_sizes(self, database):
        if not is_valid_database_param(database):
            raise ClientException(
                'Invalid character is in specified database name: `{}`'.format(database)
            )

        sql = '''
        SELECT table_name AS "Table",
            ROUND(((data_length + index_length) / 1024 / 1024), 1) AS "Size (MB)"
            FROM information_schema.TABLES
            WHERE table_schema = "{database}"
            ORDER BY (data_length + index_length) DESC;
        '''.format(
            database=database
        )
        self.run_query(sql)

    def run_query(self, sql):
        if self.socket:
            command = ['mysql', '-S', self.socket, '-e', sql]
        elif self.user:
            command = ['mysql', '-u', self.user, '-e', sql]
        else:
            raise ClientException('ソケットまたはユーザを指定してください')

        subprocess.run(command)


class ClientException(Exception):
    pass


class TestFunctions(unittest.TestCase):
    def test_is_valid_database_param__valid_name(self):
        result = is_valid_database_param('valid_name')
        self.assertTrue(result)

    def test_is_valid_database_param__invalid_name(self):
        result = is_valid_database_param('data;base')
        self.assertFalse(result)

        result = is_valid_database_param('data"base')
        self.assertFalse(result)

        result = is_valid_database_param("data'base")
        self.assertFalse(result)


class TestClient(unittest.TestCase):
    @mock.patch.object(subprocess, 'run')
    def test_run_query__socket(self, run):
        socket = 'SOCKET'
        sql = 'SELECT SUM(*) FROM table'

        client = Client()
        client.set_socket(socket)
        client.run_query(sql)
        run.assert_called_once_with(['mysql', '-S', socket, '-e', sql])

    @mock.patch.object(subprocess, 'run')
    def test_run_query__user(self, run):
        user = 'user'
        sql = 'SELECT SUM(*) FROM table'

        client = Client()
        client.set_user(user)
        client.run_query(sql)
        run.assert_called_once_with(['mysql', '-u', user, '-e', sql])

    def test_run_query__error(self):
        sql = 'SELECT SUM(*) FROM table'

        with self.assertRaises(ClientException):
            client = Client()
            client.run_query(sql)


if __name__ == '__main__':
    main()
