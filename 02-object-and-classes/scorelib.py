class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print("Print Number:", self.print_id)
        print("Composer:", self.edition.composition)
        print("Title:", self.edition.name)
        print("Composition Year:", self.edition.composition.year)
        print("Editor:", self.edition.name)
        print("Editor:", self.edition.authors)
        print("Voice:", self.edition.composition.voices)
        print("Partiture:", "yes" if self.partiture else "no")

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
