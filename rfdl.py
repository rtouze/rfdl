#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Downloader for radio france podcasts. Because they do not want to provide a
link on podcast page."""

import requests
import re
from clint.textui import progress
from argparse import ArgumentParser

CHUNK_S = 1024*1024

def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("url", help="URL of the podcast page on Radio France website")
    args = parser.parse_args()
    download(args.url)

def download(url):
    """Download podcast as mp3 from url"""
    final_file = url.split("/")[-1] + ".mp3"
    session = requests.Session()

    emission_content = session.get(url)
    # on cherche data-asset-source="https://media.radiofrance-podcast.net/podcast09/10467-18.09.2017-ITEMA_21437558-1.mp3"
    my_re = re.compile(r'data-asset-source="(https://media.radiofrance-podcast.net/.*\.mp3)"')
    search_result = my_re.search(emission_content.text)
    mp3_url = None
    if search_result:
        mp3_url = search_result.group(1)

    with open(final_file, 'bw') as output:
        print(f"Downloading {mp3_url}")
        stream = session.get(mp3_url, stream=True)
        size = int(stream.headers["Content-Length"]) if "Content-Length" in stream.headers else 0

        content_with_bar = progress.bar(
            stream.iter_content(chunk_size=CHUNK_S),
            expected_size=size/(CHUNK_S) + 1
        )
        for chunk in content_with_bar:
            output.write(chunk)

if __name__ == '__main__':
    main()
