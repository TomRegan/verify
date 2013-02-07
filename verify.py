import zipfile

it = None

class Member(object):
    def __init__(self, verifier, membername):
        self._verifier = verifier
        self._membername = membername

    def withText(self, aString):
        aFile = self._verifier.zipfile().open(self._membername)
        assert(''.join(aFile.readlines()).find(aString) >= 0)
        return self

class Verifier(object):
    def __init__(self, filename, filetype="f"):
        self._filename = filename
        self._filetype = filetype
        self._zipfile = zipfile.ZipFile(filename)

    def zipfile(self):
        return self._zipfile

    def contains(self, membername):
        self._zipfile.getinfo(membername)
        return Member(self, membername)

    def doesNotContain(self, membername):
        for eachFile in self._zipfile.infolist():
            assert(eachFile.filename != membername)

def verify(filename):
    global it 
    it = Verifier(filename)


if __name__ == '__main__':
    verify('test.zip')
    it.contains('FakeJar.jar')
    it.contains('1.txt').withText("ohai").withText("ima kitteh")
    it.contains('2.txt')
    it.contains('3.txt')
    it.contains('dir/a.txt')
    it.doesNotContain('nx.txt')
