# coding=utf-8

import scraperwiki
import lxml.html
import sqlite3

BASE_URL = 'http://www.diputadossantafe.gov.ar/web/camara/diputados'

PAGES = 5

page = 1

parsedMembers = []

while page <= PAGES:

    print 'Page ' + str(page)

    html = scraperwiki.scrape(BASE_URL + '?page=' + str(page))

    root = lxml.html.fromstring(html)
    members = root.cssselect('div[class=\'autoridad-little\']')

    for member in members:

        memberData = {}

        memberData['image'] = 'http://www.diputadossantafe.gov.ar' + member.cssselect('img')[0].attrib['src']

        name = member.cssselect('h4')[0].text

        #  This seems to be very consistently Last, First
        nameParts = name.split(', ')

        memberData['name'] = u'{} {}'.format(nameParts[1], nameParts[0])
        memberData['first_name'] = nameParts[1]
        memberData['last_name'] = nameParts[0]

        memberData['party'] = member.cssselect('h5')[0].text.replace('BLOQUE ', '')

        memberData['id'] = member.cssselect('a')[0].text

        print memberData

        parsedMembers.append(memberData)

    page += 1

print 'Counted {} Members'.format(len(parsedMembers))

try:
    scraperwiki.sqlite.execute('DELETE FROM data')
except sqlite3.OperationalError:
    pass
scraperwiki.sqlite.save(
    unique_keys=['id'],
    data=parsedMembers)
