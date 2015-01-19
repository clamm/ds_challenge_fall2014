import os
import sys

import numpy as np
from pyspark import SparkContext
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.regression import LabeledPoint
from writer import Writer


def parseLabeledPoint(line):
    label, features = line.split(',')
    label = float(label)
    features = np.array([float(x) for x in features.split(' ')])
    return LabeledPoint(label, features)

def parseVector(line):
    return np.array([float(x) for x in line.split(' ')])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage = "Usage: classify_spam_bayes <train file> <test file> <test id file>"
        print >> sys.stderr, usage
        exit(-1)
    trainFile = sys.argv[1]
    testFile = sys.argv[2]
    testIdFile = sys.argv[3]

    sc = SparkContext(appName="NaiveBayes")

    trainLines = sc.textFile(trainFile)
    print("INFO: Read lines of train data file %s" % trainFile)
    trainData = trainLines.map(parseLabeledPoint)
    print("INFO: Start training the model")
    model = NaiveBayes.train(trainData)

    testLines = sc.textFile(testFile)
    print("INFO: Read lines of test data file %s" % testFile)
    testData = testLines.map(parseVector)
    print("INFO: Predict test data")
    prediction = testData.map(model.predict).collect()

    name, extension = os.path.splitext(testFile)
    outFile = name + "_bayes_prediction" + extension
    print("INFO: Write prediction result into %s" % outFile)
    writer = Writer(outFile)
    writer.writePrediction(prediction, testIdFile)
    print("INFO: Done")
    sc.stop()


