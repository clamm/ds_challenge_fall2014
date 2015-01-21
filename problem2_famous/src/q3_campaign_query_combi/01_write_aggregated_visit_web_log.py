import json
import sys

from pyspark import SparkContext


def writeJson(outFile, logEntries):
    of = open(outFile, "w+")
    of.write(logEntries)
    of.close()


def mergeActions(docX, docY):
    assert u'action' in docX.keys(), "no 'action' in keys %s" % docX.keys()
    assert u'action' in docY.keys(), "no 'action' in keys %s" % docY.keys()
    # to keep campaign and query info
    if len(docX.keys()) >= len(docY.keys()):
        master = docX
        slave = docY
    else:
        master = docY
        slave = docX
    masterAction = getValueAsList(master, u'action')
    slaveAction = getValueAsList(slave, u'action')
    # overwrite previous value with merged list
    master[u'action'] = masterAction + slaveAction
    return master


def getValueAsList(doc, key):
    if type(doc[key]) != list:
        value = [doc[key]]
    else:
        value = doc[key]
    return value


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage = "Usage: spark-submit 01_write_aggregated_visit_web_log <in.json> <out.json>"
        print >> sys.stderr, usage
        exit(-1)
    inJson = sys.argv[1]
    outJson = sys.argv[2]

    sc = SparkContext(appName="AggregateVisits")
    lines = sc.textFile(inJson)
    data = lines.map(lambda x: json.loads(x))
    print("INFO: aggregate actions per (visit_id,uid)")
    visitUserPairRdd = data.map(lambda x: ((x[u'visit_id'], x[u'uid']), x))
    visitUserPairRdd = visitUserPairRdd.reduceByKey(lambda x, y: mergeActions(x, y))
    print("INFO: write merged actions per visit to %s" % outJson)
    visitUserPairRdd.values().map(lambda x: json.dumps(x)).saveAsTextFile(outJson)

    sc.stop()
