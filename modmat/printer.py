import os

class PrinterError(Exception):
    pass

class Printer(object):
    def __init__(self, path, npops):
        self.path = path
        self.npops = npops

        self._tick = 0
        self._data = {}

        if os.path.exists(path):
            raise PrinterError("Path '%s' exists. Aborting." % path)

        os.mkdir(path)

    def register(self, popno, data):
        self._data[popno] = data

    def tick(self):
        if len(self._data) != self.npops:
            raise PrinterError("Didn't get data for each population for tick %d!" % self.tick)

        self._print()

        self._tick += 1
        self._data = {}

    def _print(self):
        for popidx, popdata in self._data.iteritems():
            for key, data in popdata.iteritems():
                fname = os.path.join(self.path, "%s.%d" % (key, popidx))
                with open(fname, 'a') as f:
                    f.write(data)
                    f.close()
