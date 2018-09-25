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
    rCompositionYear = re.compile("Composition Year: (.*)")
    rEdition = re.compile("Edition: (.*)")
    rEditor = re.compile("Editor: (.*)")
    rVoice = re.compile("Voice (\d*): (.*)")
    rPartiture = re.compile("Partiture: (.*)")

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
        match = r1.match(n);
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

def main():
    filename = sys.argv[1]
    load(filename)


main()