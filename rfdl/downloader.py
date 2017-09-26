#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Downloader for radio france podcaast"""

import requests
import re
import sys


def main():
    print("go")
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.franceculture.fr/emissions/les-chemins-de-la-philosophie/philosophie-des-jeux-video-14-de-lantiquite-nos-jours"
    final_file = url.split("/")[-1] + ".mp3"
    response = requests.get(url)
    print(type(response.text))


    # on cherche data-asset-source="https://media.radiofrance-podcast.net/podcast09/10467-18.09.2017-ITEMA_21437558-1.mp3"
    my_re = re.compile(r'data-asset-source="(https://media.radiofrance-podcast.net/.*\.mp3)"')
    search_result = my_re.search(response.text)
    mp3_url = None
    if search_result:
        print("j'ai un result")
        mp3_url = search_result.group(1)

    with open(final_file, 'bw') as output:
        print(f"Downloading {mp3_url}")
        output.write(requests.get(mp3_url).content)
        print(f"{output.name} downloaded!")
    
    pass

if __name__ == '__main__':
    main()
