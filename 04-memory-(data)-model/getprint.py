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



def main():
    composer_substr = sys.argv[1]
    prints = load(filename)

    dbname = "./scorelib.dat"

    conn = sqlite3.connect(dbname)

    cur = conn.cursor()

    schemaFile = open('./scorelib.sql', 'r')

    sql = schemaFile.read()
    conn.executescript(sql)


    cur = conn.cursor()

    cur.execute('SELECT * FROM person WHERE person.name LIKE %?%', editionAutor)
    storedEditionAutor = cur.fetchone()

    conn.commit()

main()