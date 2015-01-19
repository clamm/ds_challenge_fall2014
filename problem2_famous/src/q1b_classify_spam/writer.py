import sys


class Writer:
    def __init__(self, outFile):
        self.outFile = outFile

    def writePrediction(self, prediction, idFile):
        i = open(idFile)
        content = i.read()
        ids = content.splitlines()
        i.close()
        if len(ids) != len(prediction):
            print >> sys.stderr, "Size mismatch of %s and prediction" % idFile
            exit(-1)

        ofile = open(self.outFile, "w+")
        for j in range(len(ids)):
            ofile.write("%s %s\n" % (ids[j], prediction[j]))
        ofile.close()