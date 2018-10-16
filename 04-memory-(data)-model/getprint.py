#!/usr/bin/env python3

import sys
import re
import sqlite3
from collections import Counter
from scorelib import Print
from scorelib import Composition
from scorelib import Person
from scorelib import Voice
from scorelib import Edition
import json

def main():
    print_id = (sys.argv[1],)

    dbname = "./scorelib.dat"

    conn = sqlite3.connect(dbname)
    dataForJson = {}

    printCursor = conn.cursor()
    printCursor.execute('SELECT * FROM print pr WHERE pr.id == ?', print_id)

    print_instance = printCursor.fetchone()
    print_id = (print_instance[0],)

    editionCursor = conn.cursor()
    editionCursor.execute('SELECT * FROM edition ed \
                                      JOIN print pr on ed.id = pr.edition \
                                      WHERE pr.id = ? ORDER BY ed.id ASC', print_id)

    edition_instance = editionCursor.fetchone()
    edition_id = (edition_instance[0],)

    editionId = (edition_instance[0],)

    compositionCursor = conn.cursor()
    compositionCursor.execute('SELECT * FROM score sc \
                                          JOIN edition ed on ed.score = sc.id \
                                          WHERE ed.id = ? ORDER BY ed.id ASC', editionId)

    conposition_instance = compositionCursor.fetchone()
    composition_id = (conposition_instance[0],)

    composerCutsor = conn.cursor()
    composerCutsor.execute('SELECT * FROM score_author sca \
                                  JOIN person p on p.id = sca.composer \
                                  WHERE sca.score = ?', composition_id)

    composers = []

    for composer in composerCutsor:
        composer_instance = {}

        composer_instance["name"] = composer[6]
        composer_instance["born"] = composer[4]
        composer_instance["died"] = composer[5]
        composers.append(composer_instance)

    dataForJson = composers

    json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)


main()