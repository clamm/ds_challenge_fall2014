import json
import sys

from pyspark import SparkContext


def writeOutputJson(outFile, ctr):
    result = json.dumps({"overall_ad_click_through_rate": ctr}, indent=True)
    of = open(outFile, "w+")
    of.write(result)
    of.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage = "Usage: compute_ctr <in.json> <out.json>"
        print >> sys.stderr, usage
        exit(-1)
    inJson = sys.argv[1]
    outJson = sys.argv[2]

    sc = SparkContext(appName="CTR")
    lines = sc.textFile(inJson)
    data = lines.map(lambda x: json.loads(x))
    nbVisitIds = data.map(lambda x: x["visit_id"]).distinct().count()
    print("INFO: There are %s unique visit_ids" % nbVisitIds)
    nbAdclicks = data.map(lambda x: x["action"]).filter(lambda s: "adclick" in s).count()
    print("INFO: There are in total %s adclicks" % nbAdclicks)
    ctr = float(nbAdclicks) / nbVisitIds
    print("INFO: The overall CTR is %f" % ctr)
    writeOutputJson(outJson, ctr)
    sc.stop()


