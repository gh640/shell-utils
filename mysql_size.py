'''MySQL データベースのサイズを取得する
'''

import argparse
import getpass
import subprocess


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
    parser = argparse.ArgumentParser(description='MySQL データベースのサイズをチェックする')
    parser.add_argument('--socket', '-S', nargs='?')
    parser.add_argument('--user', '-u', nargs='?', default=getpass.getuser())
    parser.add_argument('database', nargs='?')
    return parser


def is_valid_database_param(database_name):
    '''簡易的なインジェクション対策を行う（標準ライブラリの範囲でできることをやる）'''
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
        SELECT table_schema AS "データベース",
            ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS "サイズ (MB)"
            FROM information_schema.TABLES
            GROUP BY table_schema;
        '''
        self.run_query(sql)

    def check_table_sizes(self, database):
        if not is_valid_database_param(database):
            raise ClientException('指定されたデータベース名に不正な文字が含まれています: `{}`'.format(database))

        sql = '''
        SELECT table_name AS "テーブル",
            ROUND(((data_length + index_length) / 1024 / 1024), 1) AS "サイズ (MB)"
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


if __name__ == '__main__':
    main()
