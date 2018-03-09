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
                            [default: "arxiv-data.txt"]

"""

from docopt import docopt

import sys
import re
import urllib.request
import feedparser


def getopts(argv):
    """ Returns the command line arguments as a dictionary. """
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts


def get_data(start: int, count: int):
    """ Fetches titles from the arXiv API.

    Starts at 'start', returns at most 'count' titles.
    """
    req_url = ("http://export.arxiv.org/api/query?"
               "search_query=cat:hep-th&"
               "start=%d&max_results=%d") % (start, count)
    request = urllib.request.Request(req_url)
    data = urllib.request.urlopen(request).read()
    parsed = feedparser.parse(data)
    print(req_url)
    titles = [x.title for x in parsed.entries]

    whitespace = re.compile(r"\s+")
    titles = [whitespace.sub(" ", x) for x in titles]
    return "\n".join(titles)


if __name__ == "__main__":
    opts = docopt(__doc__, version='arxiv-data v0.1')
    start = int(opts['--start'])
    count = int(opts['--count'])
    outpath = opts['--out']
    titles = get_data(start, count)

    with open(outpath, 'w', encoding='utf8') as f:
        f.write(titles)
