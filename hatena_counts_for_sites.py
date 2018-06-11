'''Checks, hatena bookmark counts for sites.
'''

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import requests

DATA_TEMPLATE = '''
<methodCall>
<methodName>bookmark.getTotalCount</methodName>
<params>
  <param>
    <value>
      <string>{}</string>
    </value>
  </param>
</params>
</methodCall>
'''
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
    request_url = 'http://b.hatena.ne.jp/xmlrpc'
    r = requests.post(
        request_url,
        headers={'Content-Type': 'text/xml'},
        data=build_request_data(DATA_TEMPLATE, [url]),
    )
    tree = ET.fromstring(r.text)
    count = tree.find('.//int').text

    return url, count


def build_request_data(template, params):
    return template.format(*(escape(x) for x in params))


if __name__ == '__main__':
    main()
