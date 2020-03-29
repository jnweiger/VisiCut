#! /bin/sh
#

set -x

./pull_fln_wiki.py "https://wiki.fablab-nuernberg.de/w/Nova_35" > nova35.json
./pull_fln_wiki.py "https://wiki.fablab-nuernberg.de/w/ZING_4030" > zing4030.json

