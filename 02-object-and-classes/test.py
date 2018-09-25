#!/usr/bin/env python3

import sys
import re
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
    rVoice = re.compile("Voice (\d*): (.*)")
    r_partiture = re.compile("Partiture: (.*)")
    r_incipit = re.compile("Incipit: (.*)")

    prints = []

    composition = None

    for line in file:
        m = r_print_id.match(line)
        if m:
            print_id = load_print_id(m)
            print_class = Print(None, print_id, None)
            prints.append(print_class)
            continue

        m = r_composer.match(line)
        if m:
            composition_authors = load_composer(m)
            composition = Composition(None, None, None, None, None, None, composition_authors)
            continue

        m = r_title.match(line)
        if m:
            title = load_title(m)
            composition.name = title
            continue

        m = r_genre.match(line)
        if m:
            genre = load_genre(m)
            composition.genre = genre
            continue

        m = r_key.match(line)
        if m:
            key = load_key(m)
            composition.key = key
            continue

        m = r_composition_year.match(line)
        if m:
            year = load_composition_year(m)
            composition.key = year
            continue

        m = r_partiture.match(line)
        if m:
            paritture = load_partiture(m)
            Print.partiture = paritture
            continue

        m = r_incipit.match(line)
        if m:
            incipit = load_incipit(m)
            composition.key = incipit
            continue

        m = r_edition.match(line)
        if m:
            edition = load_edition(m)
            edition_class = Edition(composition, None, edition)
            continue

        m = r_editor.match(line)
        if m:
            authors = load_editor(m)
            edition_class.authors = authors
            continue




    for print_instance in prints:
        print("Print Number:", print_instance.print_id, print_instance.edition)


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

def main():
    filename = sys.argv[1]
    load(filename)


main()