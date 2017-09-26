#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rfdl

# https://www.franceculture.fr/emissions/les-chemins-de-la-philosophie/philosophie-des-jeux-video-14-de-lantiquite-nos-jours

def main():
    url = (
        "https://www.franceculture.fr/emissions/"
        "les-chemins-de-la-philosophie/"
        "philosophie-des-jeux-video-14-de-lantiquite-nos-jours"
    )
    rfdl.download(url)

if __name__ == '__main__':
    main()

