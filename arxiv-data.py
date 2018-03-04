from typing import List

import re
import urllib.request
import feedparser
request = urllib.request.Request(
    'http://export.arxiv.org/api/query?search_query=cat:hep-th&start=0&max_results=1000')
data = urllib.request.urlopen(request).read()
parsed = feedparser.parse(data)

titles: List[str] = [x.title for x in parsed.entries]

whitespace = re.compile(r"\s+")
titles = [whitespace.sub(" ", x) for x in titles]

print("\n".join(titles))
