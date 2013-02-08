import zipfile, tempfile, os, shutil

it = None

class Member(object):
    def __init__(self, parent, membername):
        self._archive = parent
        self._membername = membername
        self._tempDir = None

    def __del__(self):
        if self._tempDir:
            shutil.rmtree(self._tempDir)

    def withText(self, aString):
        aFile = self._archive.open(self._membername)
        assert(''.join(aFile.readlines()).find(aString) >= 0)
        return self

    def contains(self, filename):
        return self.whichContains(filename)

    def whichContains(self, filename):
        self._tempDir = tempfile.mkdtemp()
        self._archive.extract(
            member=self._membername, path=self._tempDir)
        return Archive(
            os.path.join(self._tempDir, self._membername)).contains(filename)


class Archive(object):
    def __init__(self, filename):
        self._archive = zipfile.ZipFile(filename)

    def contains(self, membername):
        self._archive.getinfo(membername)
        return Member(self._archive, membername)

    def doesNotContain(self, membername):
        for eachFile in self._archive.infolist():
            assert(eachFile.filename != membername)
        return self

def verify(filename):
    global it
    it = Archive(filename)
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

