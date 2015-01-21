import sys
from numpy import genfromtxt
from writer import Writer


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage = "Usage: python 03_format_result_into_json <result.csv> <out.json>\n" \
                "Example: python 03_format_result_into_json out/webAggCampaignQuery.csv ../../out/q3.json"
        print >> sys.stderr, usage
        exit(-1)
    inCsv = sys.argv[1]
    outJson = sys.argv[2]
    stringData = genfromtxt(inCsv, delimiter=",", skip_header=True, usecols=(0, 1, 6), dtype="|S50")
    campaign = [el[0] for el in stringData]
    query = [el[1] for el in stringData]
    sd = [float(el[2]) for el in stringData]
    writer = Writer(outJson)
    formattedMean = writer.formatMeanResult(campaign[0], query[0])
    formattedSd = writer.formatStandardDeviationResult(campaign, query, sd)
    result = writer.combineMeanAndStandardDeviation(formattedMean, formattedSd)
    writer.writeResult(result)