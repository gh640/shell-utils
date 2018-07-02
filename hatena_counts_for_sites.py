'''Checks hatena bookmark counts for sites.
'''

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import unittest
from unittest import mock

import requests

MAX_WORKERS = 5


def main():
    args = get_args()
    results = get_hatena_counts_async(args.url)
    for url, count in results:
        print('{}\t{}'.format(url, count))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='+', help='urls to check the counts of.')
    return parser.parse_args()


def get_hatena_counts_async(urls):
    with ThreadPoolExecutor(MAX_WORKERS) as executor:
        futures = (executor.submit(get_hatena_count_for_site, url)
                   for url in urls)
        return [t.result() for t in as_completed(futures)]

    return []


def get_hatena_count_for_site(url):
    request_url = 'http://api.b.st-hatena.com/entry.total_count'
    payload = {'url': url}
    r = requests.get(request_url, params=payload)
    count = r.json()['total_bookmarks']

    return url, count


class TestGetHatenaCountsAsync(unittest.TestCase):
    @mock.patch('hatena_counts_for_sites.get_hatena_count_for_site')
    def test_with_mock(self, func):
        dummy_result = 'url', 5
        count = 20
        func.return_value = dummy_result
        results = get_hatena_counts_async(['dummy_url'] * count)
        self.assertEquals(results, [dummy_result] * count)


class TestGetHatenaCountForSite(unittest.TestCase):
    def test_google(self):
        url_req = 'https://www.google.co.jp'
        url, count = get_hatena_count_for_site(url_req)
        self.assertEquals(url, url_req)
        self.assertIsInstance(count, int)


if __name__ == '__main__':
    main()
