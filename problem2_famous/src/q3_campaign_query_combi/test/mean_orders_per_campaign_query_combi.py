import json
import sys
import operator

from pyspark import SparkContext
from writer import Writer

# THIS WAS A SUCCESSFUL ATTEMPT TO CALCULATE THE MEAN ORDERS PER CAMPAIGN-QUERY COMBINATION
# HOWEVER THIS AND THE STANDARD DEVIATION CALCULATION CAN BE DONE WITH A ONE-LINER IN R (ONCE WE PRODUCED THE
# AGGREGATED VISIT DATA IN SPARK)


def dropUnusedKeys(doc, keys):
    for key in keys:
        if key in doc.keys():
            del (doc[key])
    return doc


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


def combineUidsAndCountOrders(docX, docY):
    uids = getListValuesFromDocs(docX, docY, u'uid')
    actions = getListValuesFromDocs(docX, docY, u'action')
    nbOrders = actions.count(u'order')
    assert docX[u'campaign'] == docY[u'campaign']
    assert docX[u'query'] == docY[u'query']
    return {u'campaign': docX[u'campaign'], u'query': docX[u'query'], u'uid': uids, u'nbOrders': nbOrders,
            u'action': [u'order' for x in range(nbOrders)]}


def getListValuesFromDocs(docX, docY, key):
    assert key in docX.keys(), "no '%s' in keys %s" % (key, docX.keys())
    assert key in docY.keys(), "no '%s' in keys %s" % (key, docY.keys())
    docXvalue = getValueAsList(docX, key)
    docYvalue = getValueAsList(docY, key)
    return docXvalue + docYvalue


def calculateMeanOrderPerVisitor(doc):
    nbOrders = doc[u'nbOrders']
    nbVisitors = len(set(doc[u'uid']))
    meanOrdersPerVisitor = nbOrders / float(nbVisitors)
    return {u'campaign': doc[u'campaign'], u'query': doc[u'query'],
            u'meanOrdersPerVisitor': meanOrdersPerVisitor}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage = "Usage: spark-submit mean_orders_per_campaign_query_combi <in.json> <out.json>"
        print >> sys.stderr, usage
        exit(-1)
    inJson = sys.argv[1]
    outJson = sys.argv[2]

    sc = SparkContext(appName="CampaignQueryCombinations")
    lines = sc.textFile(inJson)
    data = lines.map(lambda x: json.loads(x))
    print("INFO: aggregate actions per (visit_id,uid)")
    visitUserPairRdd = data.map(lambda x: ((x[u'visit_id'], x[u'uid']), x))
    cleanVisitUserPairRdd = visitUserPairRdd.mapValues(lambda x: dropUnusedKeys(x, [u'tstamp', u'experiments']))
    cleanVisitUserPairRdd = cleanVisitUserPairRdd.reduceByKey(lambda x, y: mergeActions(x, y))
    print("INFO: collect uids and count orders per (campaign,query)")
    campaignQueryPairRDD = cleanVisitUserPairRdd.values().map(lambda x: ((x[u'campaign'], x[u'query']), x))
    campaignQueryPairRDD = campaignQueryPairRDD.reduceByKey(lambda x, y: combineUidsAndCountOrders(x, y))
    print("INFO: compute mean order per visitor within (campaign,query)")
    campaignQueryPairRDD = campaignQueryPairRDD.mapValues(lambda x: calculateMeanOrderPerVisitor(x))
    means = campaignQueryPairRDD.values().collect()
    max_index, max_value = max(enumerate([doc[u'meanOrdersPerVisitor'] for doc in means]), key=operator.itemgetter(1))
    bestMean = means[max_index]
    print("INFO: out of %s (campaign,query) combinations the best mean order per visitor is %f within "
          "(campaign=%s,query=%s)" % (len(means), max_value, bestMean[u'campaign'], bestMean[u'query']))
    listOfStandardDeviations = []
    writer = Writer(outJson)
    writer.writeOutputJson(bestMean, listOfStandardDeviations)
    sc.stop()


# run with: (takes about 5 minutes on Mac)
# spark-submit mean_orders_per_campaign_query_combi.py ../../../data/web.log ../../../out/q3.json

