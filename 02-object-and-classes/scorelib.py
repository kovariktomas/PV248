class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print("Print Number:", self.print_id)

        if self.edition.composition.authors:
            first = True
            for author in self.edition.composition.authors:
                if author.name and first:
                    first = False
                    print("Composer: ", end='')
                else:
                    print("; ", end='')

                if author.name:
                    print (author.name, sep='', end='')
                if ((not (author.born == None)) and (not (author.died == None))):
                    print (" (", author.born, "--", author.died, ")", end='', sep='')
                elif author.born:
                    print (" (", author.born, "--)", end='', sep='')
                elif author.died:
                    print (" (--", author.died, ")", end='', sep='')

            print ("")

        if self.edition.composition.name:
            print("Title:", self.edition.composition.name)
        if self.edition.composition.genre:
            print("Genre:", self.edition.composition.genre)
        if self.edition.composition.key:
            print("Key:", self.edition.composition.key)
        if self.edition.composition.year:
            print("Composition Year:", self.edition.composition.year)
        if self.edition.name:
            print("Edition:", self.edition.name)

        first = True
        if self.edition.authors:
            for author in self.edition.authors:
                if author.name and first:
                    first = False
                    print("Editor: ", end='')
                else:
                    print("; ", end='')

                if author.name:
                    print (author.name, sep='', end='')
                if ((not (author.born == None)) and (not (author.died == None))):
                    print (" (", author.born, "--", author.died, ")", end='', sep='')
                elif author.born:
                    print (" (", author.born, "--)", end='', sep='')
                elif author.died:
                    print (" (--", author.died, ")", end='', sep='')

            print ("")

        if self.edition.composition.voices:
            first = True
            i = 1
            for voice in self.edition.composition.voices:
                print("Voice ", i, ": ", sep='', end='')
                i = i + 1
                if voice.range:
                    print (voice.range, sep='', end='')
                if voice.name:
                    print ("; ", voice.name, sep='', end='')
                print ("")

        if not (self.partiture == None):
            print("Partiture:", "yes" if self.partiture else "no")

        if self.edition.composition.incipit:
            print("Incipit:", self.edition.composition.incipit)

        print("")

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = authors
        self.name = name


class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors


class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range


class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died
