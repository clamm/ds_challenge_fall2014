import os
import sys

import numpy as np
from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans
from writer import Writer


def parseVector(line):
    return np.array([float(x) for x in line.split(' ')])


if __name__ == "__main__":
    if len(sys.argv) != 5:
        usage = "Usage: classify_spam_kmeans <train file> <k> <test file> <test id file>"
        print >> sys.stderr, usage
        exit(-1)
    trainFile = sys.argv[1]
    k = int(sys.argv[2])
    testFile = sys.argv[3]
    testIdFile = sys.argv[4]

    sc = SparkContext(appName="KMeans")

    trainLines = sc.textFile(trainFile)
    print("INFO: Read lines of train data file %s" % trainFile)
    trainData = trainLines.map(parseVector)
    print("INFO: Start training the model with k=%i" % k)
    model = KMeans.train(trainData, k)
    print("Final cluster centers: %s" % model.clusterCenters)

    testLines = sc.textFile(testFile)
    print("INFO: Read lines of test data file %s" % testFile)
    testData = testLines.map(parseVector)
    print("INFO: Predict test data")
    prediction = testData.map(model.predict).collect()

    name, extension = os.path.splitext(testFile)
    outFile = name + "_kmeans_prediction" + extension
    print("INFO: Write prediction result into %s" % outFile)
    writer = Writer(outFile)
    writer.writePrediction(prediction, testIdFile)
    print("INFO: Done")
    sc.stop()


