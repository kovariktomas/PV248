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


def load(filename):

    file = open(filename, 'r')

    r_print_id = re.compile("Print Number: (.*)")
    r_composer = re.compile("Composer: (.*)")
    r_title = re.compile("Title: (.*)")
    r_genre = re.compile("Genre: (.*)")
    r_key = re.compile("Key: (.*)")
    r_composition_year = re.compile("Composition Year: (.*)")
    r_edition = re.compile("Edition: (.*)")
    r_editor = re.compile("Editor: (.*)")
    r_voice = re.compile("Voice (\d*): (.*)")
    r_partiture = re.compile("Partiture: (.*)")
    r_incipit = re.compile("Incipit: (.*)")

    r_new_entity = re.compile("\n")
    prints = []

    voices = []
    composition_class = Composition(None, None, None, None, None, None, None)
    edition_class = Edition(None, None, None)
    print_class = Print(None, None, None)


    for line in file:
        m = r_print_id.match(line)
        if m:
            print_id = load_print_id(m)
            print_class.print_id = print_id
            continue

        m = r_composer.match(line)
        if m:
            composition_authors = load_composer(m)
            composition_class.authors = composition_authors
            continue

        m = r_title.match(line)
        if m:
            title = load_title(m)
            composition_class.name = title
            continue

        m = r_genre.match(line)
        if m:
            genre = load_genre(m)
            composition_class.genre = genre
            continue

        m = r_key.match(line)
        if m:
            key = load_key(m)
            composition_class.key = key
            continue

        m = r_composition_year.match(line)
        if m:
            year = load_composition_year(m)
            composition_class.year = year
            continue

        m = r_partiture.match(line)
        if m:
            paritture = load_partiture(m)
            print_class.partiture = paritture
            continue

        m = r_incipit.match(line)
        if m:
            incipit = load_incipit(m)
            composition_class.incipit = incipit
            continue

        m = r_edition.match(line)
        if m:
            edition = load_edition(m)
            edition_class.name = edition
            continue

        m = r_editor.match(line)
        if m:
            authors = load_editor(m)
            edition_class.authors = authors
            continue

        m = r_voice.match(line)

        if m:
            voice = load_voice(m)
            voices.append(voice)
            composition_class.voices = voices
            continue

        m = r_new_entity.match(line)
        if m:
            edition_class.composition = composition_class
            print_class.edition = edition_class
            if not (print_class.print_id == None):
                prints.append(print_class)

                voices = []
                composition_class = Composition(None, None, None, None, None, None, None)
                edition_class = Edition(None, None, None)
                print_class = Print(None, None, None)

            continue

    return prints


def load_print_id(match):
    print_id = match.group(1).strip()
    return print_id


def load_composer(match):
    composers = []
    r1 = re.compile("(.*)(\((\+)*\d{4}(.*)\)){1}")
    r_borned = re.compile("\((\+)*(\d{4})(.*)")
    r_died = re.compile("(.*)(\d{4})(.*)")
    name = match.group(1).strip()
    for n in name.split(';'):
        match = r1.match(n)
        if match:
            person_name = match.group(1).strip()
            match_borned = r_borned.match(match.group(2).strip())
            if match_borned:
                if (match_borned.group(1) == "+"):
                    borned = None
                    died = match_borned.group(2).strip()
                else:
                    borned = match_borned.group(2).strip()
                    match_died = r_died.match(match_borned.group(3).strip())
                    if match_died:
                        died = match_died.group(2).strip()
                    else:
                        died = None
            else:
                borned = None
                died = None
            composers.append(Person(person_name, borned, died))
        elif (not (n == "")):
            composers.append(Person(n, None, None))

    return composers


def load_title(match):
    title = match.group(1).strip()
    if (not (title == "")):
        return title
    else:
        return None

def load_genre(match):
    genre = match.group(1).strip()
    if (not (genre == "")):
        return genre
    else:
        return None

def load_key(match):
    key = match.group(1).strip()
    if (not (key == "")):
        return key
    else:
        return None

def load_composition_year(match):
    m = match.group(1).strip()
    r1 = re.compile("(.*)(\d{4})(.*)")
    if (not (m == "")):
        year = r1.match(m)
        if year:
            return int(year.group(2).strip())
    else:
        return None


def load_edition(match):
    edition = match.group(1).strip()
    if (not (edition == "")):
        return edition
    else:
        return None


def load_editor(match):
    editors = []
    r1 = re.compile("(.*)(\((\+)*\d{4}(.*)\)){1}")
    r_borned = re.compile("\((\+)*(\d{4})(.*)")
    r_died = re.compile("(.*)(\d{4})(.*)")
    name = match.group(1).strip()
    for n in name.split(';'):
        match = r1.match(n)
        if match:
            person_name = match.group(1).strip()
            match_borned = r_borned.match(match.group(2).strip())
            if match_borned:
                if (match_borned.group(1) == "+"):
                    borned = None
                    died = match_borned.group(2).strip()
                else:
                    borned = match_borned.group(2).strip()
                    match_died = r_died.match(match_borned.group(3).strip())
                    if match_died:
                        died = match_died.group(2).strip()
                    else:
                        died = None
            else:
                borned = None
                died = None
            editors.append(Person(person_name, borned, died))
        elif (not (n == "")):
            editors.append(Person(n, None, None))

    return editors


def load_partiture(match):
    partiture = match.group(1).strip()
    r1 = re.compile("(.*)yes(.*)")
    if (not (partiture == "")):
        match = r1.match(partiture)
        if match:
            return True
        return False
    else:
        return False

def load_incipit(match):
    incipit = match.group(1).strip()
    if (not (incipit == "")):
        return incipit
    else:
        return None


def load_voice(match):
    voice = match.group(2).strip()
    r1 = re.compile("((.*)--(.*))")
    r2 = re.compile("(None)")

    range = ""
    name = ""

    if (not (voice == "")):
        for n in voice.split(';'):
            for m in n.split(','):
                voice_item = m.strip()
                match = r1.match(voice_item)
                match1 = r2.match(voice_item)
                if match:
                    range = (match.group(0)) if range == "" else (range + ", " + match.group(0))
                elif match1:
                    range = ""
                else:
                    name = m.strip() if name == "" else (name + ", " + m.strip())

    return Voice(name if not (name == "") else None, range if not (range == "") else None)


#insert person and check duplicity
def insertPerson(autor, cur):
    personName = (autor.name,)
    cur.execute('SELECT * FROM person WHERE name=?', personName)
    storedPerson = cur.fetchone()
    if storedPerson == None:
        person = (
        autor.name, "NULL" if autor.born == None else autor.born, "NULL" if autor.died == None else autor.died)
        cur.execute('INSERT INTO person ("name", "born", "died") VALUES (?,?,?)', person)
        return cur.lastrowid
    else:
        if storedPerson[1] == "NULL" and autor.born != None:
            cur.execute('UPDATE person SET "born" = ? WHERE name = ?', (autor.born, autor.name))
        if storedPerson[2] == "NULL" and autor.died != None:
            cur.execute('UPDATE person SET "died" = ? WHERE name = ?', (autor.died, autor.name))
        return storedPerson[0]



def insertScore(print_instance, cur):
    name = "NULL" if print_instance.edition.composition.name == None else print_instance.edition.composition.name
    genre = "NULL" if print_instance.edition.composition.genre == None else print_instance.edition.composition.genre
    key = "NULL" if print_instance.edition.composition.key == None else print_instance.edition.composition.key
    incipit = "NULL" if print_instance.edition.composition.incipit == None else print_instance.edition.composition.incipit
    year = "NULL" if print_instance.edition.composition.year == None else print_instance.edition.composition.year

    score = (name, genre, key, incipit, year)

    cur.execute('SELECT * FROM score WHERE name=? and genre=? and key=? and incipit=? and year=?', score)
    storedScore = cur.fetchone()
    if storedScore == None:
        cur.execute('INSERT INTO score ("name", "genre", "key", "incipit", "year") VALUES (?,?,?,?,?)', score)
        return cur.lastrowid
    else:
        return storedScore[0]


def insertVoice(voice, number, scoreId, cur):

    name = "NULL" if voice.name == None else voice.name
    range = "NULL" if voice.range == None else voice.range

    voice = (name, range, number, scoreId)

    cur.execute('SELECT * FROM voice WHERE name=? and range=? and number=? and score=?', voice)
    storedScore = cur.fetchone()
    if storedScore == None:
        cur.execute('INSERT INTO voice ("name", "range", "number", "score") VALUES (?,?,?,?)', voice)
        return cur.lastrowid
    else:
        return storedScore[0]

def insertEdition(print_instance, scoreId, cur):

    name = "NULL" if print_instance.edition.name == None else print_instance.edition.name

    year = "NULL"

    edition = (name, year, scoreId)

    cur.execute('SELECT * FROM edition WHERE name=? and year=? and score=?', edition)
    storedEdition = cur.fetchone()
    if storedEdition == None:
        cur.execute('INSERT INTO edition ("name", "year", "score") VALUES (?,?,?)', edition)
        return cur.lastrowid
    else:
        return storedEdition[0]


def insertScoreAutor(composerId, scoreId, cur):

    scoreAutor = (composerId, scoreId)

    cur.execute('SELECT * FROM score_author WHERE composer=? and score=?', scoreAutor)
    storedScoreAutor = cur.fetchone()
    if storedScoreAutor == None:
        cur.execute('INSERT INTO score_author ("composer", "score") VALUES (?,?)', scoreAutor)
        return cur.lastrowid
    else:
        return storedScoreAutor[0]


def insertEditionAutor(editorId, editionId, cur):

    editionAutor = (editorId, editionId)

    cur.execute('SELECT * FROM edition_author WHERE editor=? and edition=?', editionAutor)
    storedEditionAutor = cur.fetchone()
    if storedEditionAutor == None:
        cur.execute('INSERT INTO edition_author ("editor", "edition") VALUES (?,?)', editionAutor)
        return cur.lastrowid
    else:
        return storedEditionAutor[0]

def insertPrint(print_instance, editionId, cur):

    id = "NULL" if print_instance.print_id == None else print_instance.print_id

    partiture = "Y" if print_instance.partiture else "N"

    printRow = (id, partiture, editionId)

    cur.execute('SELECT * FROM print WHERE id=? and partiture=? and edition=?', printRow)
    storedPrint = cur.fetchone()
    if storedPrint == None:
        cur.execute('INSERT INTO print ("id", "partiture", "edition") VALUES (?,?,?)', printRow)
        return cur.lastrowid
    else:
        return storedPrint[0]

def main():
    filename = sys.argv[1]
    prints = load(filename)

    dbname = sys.argv[2]

    open(dbname, 'w').close()

    conn = sqlite3.connect(dbname)

    cur = conn.cursor()

    schemaFile = open('./scorelib.sql', 'r')

    sql = schemaFile.read()
    conn.executescript(sql)


    for print_instance in prints:

        #insert persons (composers)
        if print_instance.edition.composition.authors:
            composersId = []
            for autor in print_instance.edition.composition.authors:
                cur = conn.cursor()
                composersId.append(insertPerson(autor, cur))
                conn.commit()
        # insert persons (editors)
        if print_instance.edition.authors:
            editorsId = []
            for autor in print_instance.edition.authors:
                cur = conn.cursor()
                editorsId.append(insertPerson(autor, cur))
                conn.commit()

        #insert score
        cur = conn.cursor()
        scoreId = insertScore(print_instance, cur)
        conn.commit()

        #insert voices
        cur = conn.cursor()

        if print_instance.edition.composition.voices:
            voicesId = []
            i = 1;
            for voice in print_instance.edition.composition.voices:
                voicesId.append(insertVoice(voice, i, scoreId, cur))
                i += 1
            conn.commit()

        #insert edition

        cur = conn.cursor()
        editionId = insertEdition(print_instance, scoreId, cur)
        conn.commit()


        #insert score_autor
        cur = conn.cursor()
        for composerId in composersId:
            insertScoreAutor(composerId, scoreId, cur)

        conn.commit()

        #insert edition_autor
        cur = conn.cursor()
        for editorId in editorsId:
            insertEditionAutor(editorId, editionId, cur)

        conn.commit()

        #insert print

        cur = conn.cursor()
        printId = insertPrint(print_instance, editionId, cur)
        conn.commit()

main()