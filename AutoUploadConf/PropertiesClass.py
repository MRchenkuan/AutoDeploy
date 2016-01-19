class Properties():
    def __init__(self, path):
        self.path = path
        self.fo = open(path, 'r')
        self.lines = self.fo.readlines()
        self.fo.close()

    def set(self, key, val):
        flen = len(self.lines) - 1
        for i in range(flen):
            line = self.lines[i]
            if (line.find("=") > 0):
                _key = line.split("=")[0].strip()
                if (_key == key):
                    self.lines[i] = _key + "=" + val + "\n"

    def close(self):
        fo = open(self.path, 'w')
        fo.writelines(self.lines)
        fo.close()
