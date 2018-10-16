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
    composer_substr = ("%"+sys.argv[1]+"%",)

    dbname = "./scorelib.dat"

    conn = sqlite3.connect(dbname)
    dataForJson = {}

    composerCursor = conn.cursor()
    composerCursor.execute('SELECT * FROM person p WHERE p.name LIKE ? ORDER BY p.name ASC', composer_substr)

    for composer in composerCursor:

        #pomocny print
        #print("composer:", end=" ")
        #print(composer)

        #zaznamy pro composera
        prints = []
        # composer name
        dataForJson[composer[3]] = prints


        composerId = (composer[0], )
        compositionCutsor = conn.cursor()
        compositionCutsor.execute('SELECT * FROM score_author sca \
                               JOIN score sc on sc.id = sca.score \
                               WHERE sca.composer = ? ORDER BY sca.composer ASC', composerId)

        for composition in compositionCutsor:
            compositionId = (composition[0],)


            #pomocny print
            #print("composition:", end=" ")
            #print(composition)


            editionCursor = conn.cursor()
            editionCursor.execute('SELECT * FROM edition ed \
                                   JOIN score sc on ed.score = sc.id \
                                   WHERE ed.score = ? ORDER BY ed.id ASC', compositionId)
            for edition in editionCursor:
                editionId = (edition[0],)

                #  #pomocny print
                #print("Edition:")
                #print(edition)



                editionAuthorCursor = conn.cursor()
                editionAuthorCursor.execute('SELECT * FROM edition_author eda \
                                               JOIN person p on eda.editor = p.id \
                                               WHERE eda.edition = ? ORDER BY eda.editor ASC', editionId)
                editor = ""
                i = 0
                editionAuthors = editionAuthorCursor.fetchall()
                cnt = len(editionAuthors)
                for editionAuthor in editionAuthors:
                    #print ("row", cnt)
                    editor += editionAuthor[6]
                    if editionAuthor[4] != "NULL":
                        editor += "(" + str(editionAuthor[4]) + "-"
                        if editionAuthor[5] != "NULL":
                            editor += str(editionAuthor[5]) + ")"
                        else:
                            editor += " )"
                    elif editionAuthor[5] != "NULL":
                         editor += "( -" + str(editionAuthor[5]) + ")"

                    i += 1
                    if not (cnt == i):
                        editor += "; "

                    # pomocny print
                    #print("EditionAutor:", i)
                    #print(editionAuthor)



                printCursor = conn.cursor()
                printCursor.execute('SELECT * FROM print pr \
                                       JOIN edition e on pr.edition = e.id \
                                       WHERE pr.edition = ? ORDER BY pr.edition ASC', editionId)
                print_entity = printCursor.fetchone()
                # pomocny print
                #print("Print:")
                #print(print_entity)


            voiceCursor = conn.cursor()
            voiceCursor.execute('SELECT * FROM voice vo \
                                               JOIN score sc on vo.score = sc.id \
                                               WHERE vo.score = ? ORDER BY vo.number ASC', compositionId)

            print_instance = {}
            print_instance["Print Number"] = print_entity[0]
            print_instance["Title"] = composition[4]
            print_instance["Genre"] = composition[5]
            print_instance["Key"] = composition[6]
            print_instance["Composition Year"] = composition[8]

            print_instance["Publication Year"] = edition[3]
            print_instance["Edition"] = edition[2]
            print_instance["Editor"] = editor

            for voice in voiceCursor:
                print_instance["Voice "+ str(voice[1])] = voice[3] + "; " + voice[4]

                #pomocny print
                #print("Voice:")
                #print(voice)
            print_instance["Partiture"] = print_entity[1]
            print_instance["Incipit"] = composition[7]
            prints.append(print_instance)

        #print(" ")

    json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)
    #print(json.dump(dataForJson, sys.stdout, indent=4))

main()