import zipfile, tempfile, os, shutil

it = None

class Member(object):
    def __init__(self, parent, membername):
        self._parent = parent
        self._membername = membername

    def withText(self, aString):
        aFile = self._parent.zipfile().open(self._membername)
        assert(''.join(aFile.readlines()).find(aString) >= 0)
        return self

    def contains(self, filename):
        return self.whichContains(filename)

    def whichContains(self, filename):
        tempDir = tempfile.mkdtemp()
        self._parent.zipfile().extract(
            member=self._membername, path=tempDir)
        return Verifier(
            os.path.join(tempDir, self._membername)).contains(filename)


class Verifier(object):
    def __init__(self, filename):
        self._filename = filename
        self._zipfile = zipfile.ZipFile(filename)

    def zipfile(self):
        return self._zipfile

    def contains(self, membername):
        self._zipfile.getinfo(membername)
        return Member(self, membername)

    def doesNotContain(self, membername):
        for eachFile in self._zipfile.infolist():
            assert(eachFile.filename != membername)
        return self

def verify(filename):
    global it
    it = Verifier(filename)
    return it


if __name__ == '__main__':
    verify('test.zip')
    it.contains('1.txt').withText("ohai").withText("ima kitteh")
    it.contains('2.txt')
    it.contains('3.txt')
    it.contains('dir/a.txt')
    it.doesNotContain('nx.txt')

    jar = it.contains('FakeJar.jar')
    jar.contains("MANIFEST.MF").withText("ohai")
    jar.contains('com/caplin/java/fake.class')

