""" arXiv-data
A module to fetch high energy theoretical physics papers from arXiv.org.

Usage:
    arxiv-data.py [-s=<start>] [-o=<out>] [-c=<count>]
    arxiv-data.py (-h | --help)
    arxiv-data.py --version

Options:
    -h --help               Show this screen.
    --version               Show version.
    --start -s=<start>      Set request start.
                            [default: 0]
    --count -c=<count>      Set maximum number of titles.
                            [default: 1000]
    --out -o=<out>          Set output file.
                            [default: arxiv-data.txt]

"""

from docopt import docopt

import feedparser
import sys
import time
import re
import urllib.request


def get_data(start: int, count: int):
    """ Fetches titles from the arXiv API.

    Starts at 'start', returns at most 'count' titles.
    """
    MAX_REQUEST_SIZE = 250  # https://arxiv.org/help/api/user-manual#paging
    REQUEST_DELAY = 3  # seconds
    titles = []
    while True:
        max_results = min(count, MAX_REQUEST_SIZE)
        req_url = ("http://export.arxiv.org/api/query?"
                   "search_query=cat:hep-th&"
                   "start=%d&max_results=%d") % (start, max_results)

        print(req_url)
        request = urllib.request.Request(req_url)
        data = urllib.request.urlopen(request).read()
        start_time = time.time()
        parsed = feedparser.parse(data)
        count -= MAX_REQUEST_SIZE
        start += MAX_REQUEST_SIZE
        if(len(parsed.entries) == 0):
            break
        titles.extend([x.title for x in parsed.entries])
        if(count <= 0):
            break
        elapsed_time = time.time() - start_time
        time.sleep(REQUEST_DELAY - elapsed_time)

    whitespace = re.compile(r"\s+")
    titles = [whitespace.sub(" ", x) for x in titles]
    return "\n".join(titles)


def write_to_file(data: str, path: str):
    """ Writes the data to the given path, encoded as utf8 """
    with open(path, 'w', encoding='utf8') as f:
        f.write(data)


if __name__ == "__main__":
    opts = docopt(__doc__, version='arxiv-data v0.1')
    start = int(opts['--start'])
    count = int(opts['--count'])
    outpath = opts['--out']
    titles = get_data(start, count)
    write_to_file(titles, outpath)
