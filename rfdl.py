#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Downloader for radio france podcasts. Because they do not want to provide a
link on podcast page."""

import requests
import re
from clint.textui import progress
from argparse import ArgumentParser
import sys

CHUNK_S = 1024*1024

session = requests.Session()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("url", help="URL of the podcast page on Radio France website")
    args = parser.parse_args()
    download(args.url)

def download(url):
    """Download podcast as mp3 from url"""
    final_file = url.split("/")[-1] + ".mp3"
    mp3_url = get_mp3_url(url)
    if not mp3_url:
        print(f"No mp3 found in page {url}...")
        sys.exit(1)
    download_mp3_to_file(mp3_url, final_file)


def get_mp3_url(url):
    """Retrieve podcast mp3 url from broadcast page url """
    emission_content = session.get(url)
    # We are looking for
    # data-asset-source="https://media.radiofrance-podcast.net/some/path.mp3"
    # for France Culture pr
    # data_url="https://media.radiofrance-podcast.net/some/path.mp3" for France
    # Inter
    my_re = re.compile(
        r'data-(?:asset-source|url)='
        r'"(https://media.radiofrance-podcast.net/.*\.mp3)"'
    )
    search_result = my_re.search(emission_content.text)
    return search_result.group(1) if search_result else None


def download_mp3_to_file(mp3_url, final_file):
    """Create the file from downloaded data,"""

    with open(final_file, 'wb') as output:
        print(f"Downloading {mp3_url}")
        stream = session.get(mp3_url, stream=True)
        size = (
            int(stream.headers["Content-Length"]) 
            if "Content-Length" in stream.headers else 0
        )

        content_with_bar = progress.bar(
            stream.iter_content(chunk_size=CHUNK_S),
            expected_size=size/(CHUNK_S) + 1
        )

        for chunk in content_with_bar:
            output.write(chunk)

if __name__ == '__main__':
    main()
