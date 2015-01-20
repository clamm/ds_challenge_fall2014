import json
import sys

from pyspark import SparkContext


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage = "Usage: compute_ctr <file.json>"
        print >> sys.stderr, usage
        exit(-1)
    jsonFile = sys.argv[1]

    sc = SparkContext(appName="CTR")
    lines = sc.textFile(jsonFile)
    data = lines.map(lambda x: json.loads(x))
    nbVisitIds = data.map(lambda x: x["visit_id"]).distinct().count()
    print("INFO: There are %s unique visit_ids" % nbVisitIds)
    nbAdclicks = data.map(lambda x: x["action"]).filter(lambda s: "adclick" in s).count()
    print("INFO: There are in total %s adclicks" % nbAdclicks)
    ctr = float(nbAdclicks) / nbVisitIds
    print("INFO: The overall CTR is %f" % ctr)
    sc.stop()


