#! /usr/bin/python3
#
# References:
# - https://www.crummy.com/software/BeautifulSoup/bs4/doc
#
# (C) 2020 jnweiger@gmail.com, distribute under GPLv2 or ask.
#
# V1.0 -- 2020-03-27 jw, initial draught

from bs4 import BeautifulSoup
import requests
import sys, json

if len(sys.argv) < 2 or sys.argv[1][0] == '-':
  print("""Usage:
        %s URL > tabledump.json

Where URL is e.g. 
        "https://wiki.fablab-nuernberg.de/w/Nova_35"
        "https://wiki.fablab-nuernberg.de/w/ZING_4030"
""" % sys.argv[0], file=sys.stderr)
  sys.exit(1)

url = sys.argv[1]
r = requests.get(url)

if r.status_code != 200:
  print("Error: %s, status=%d\n" % (url, r.status_code))
  sys.exit(1)
r.close()
# now we have type(r.text) == str, and type(r.content) == bytes.

parsed_html = BeautifulSoup(r.text, "html.parser")

print("// FROM:", url)
tables = list(map(lambda x: { 'soup': x }, parsed_html.find_all('table')))
print("found %d tables" % len(tables), file=sys.stderr)


def strnum(s):
  """ convert a string to float or int if possible """
  try:
    return int(s)
  except:
    try:
      return float(s)
    except:
      pass
  return str(s)


for tab in tables:
  try: 
    tab['headline'] = tab['soup'].find_previous(attrs="mw-headline").text
  except:
    tab['headline'] = ''
  if len(tab['headline']):
    th = list(map(lambda x: x.text.strip().translate({0xa0:' '}), tab['soup'].find_all('th')))
    print("Headline:", tab['headline'], file=sys.stderr)
    rows = []
    for tr in tab['soup'].find_all('tr'):
      td = tr.find_all('td')
      if len(td) and len(td[0].text.strip()):       # skip th lines, and lines with no material. Separator lines.
        row = {}
        for i in range(len(td)):
          row[th[i]] = strnum(td[i].text.strip())
        rows.append(row)
    tab['row'] = rows

for tab in tables:      # strip the soup from the tables. We don't need them any more.
  del tab['soup']

tables = list(filter(lambda x: x['headline'] != '', tables))    # strip tables without headline
print(json.dumps(tables, indent=2, sort_keys=False)) 

