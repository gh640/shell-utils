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
    for result in results:
        print('{}\t{}'.format(result['url'], result['total_bookmarks']))


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

    return r.json()


class TestGetHatenaCountsAsync(unittest.TestCase):
    @mock.patch('hatena_counts_for_sites.get_hatena_count_for_site')
    def test_with_mock(self, func):
        dummy_result = {
            'url': 'url',
            'total_bookmarks': 5,
        }
        count = 20
        func.return_value = dummy_result
        results = get_hatena_counts_async(['dummy_url'] * count)
        self.assertEqual(results, [dummy_result] * count)


class TestGetHatenaCountForSite(unittest.TestCase):
    def test_google(self):
        url_req = 'https://www.google.co.jp'
        result = get_hatena_count_for_site(url_req)
        self.assertEqual(len(result), 2)
        self.assertIn('url', result)
        self.assertIn('total_bookmarks', result)
        self.assertEqual(result['url'], url_req)
        self.assertIsInstance(result['total_bookmarks'], int)
        self.assertTrue(result['total_bookmarks'] > 0)


if __name__ == '__main__':
    main()
