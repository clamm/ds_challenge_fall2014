import json


class Writer:
    def __init__(self, outFile):
        self.outFile = outFile

    def writeResult(self, result):
        of = open(self.outFile, "w+")
        of.write(result)
        of.close()

    def toString(self, doc):
        return json.dumps(doc, indent=True, sort_keys=True)

    def formatSparkResult(self, bestMeanCampaignQuery, listOfStandardDeviations):
        bestMeanCampaignQuery[u'query_string'] = bestMeanCampaignQuery.pop(u'query')
        del (bestMeanCampaignQuery[u'meanOrdersPerVisitor'])
        result = self.toString({"highest_mean_value": bestMeanCampaignQuery,
                                "standard_deviations": listOfStandardDeviations})
        return result

    def formatMeanResult(self, campain, query):
        return {"highest_mean_value": {"campaign": campain, "query_string": query}}

    def formatStandardDeviationResult(self, campaigns, queries, standardDeviations):
        assert len(campaigns) == len(queries) == len(standardDeviations)
        subresult = []
        for i in range(len(campaigns)):
            subresult.append({"campaign": campaigns[i],
                              "query_string": queries[i],
                              "standard_deviation": standardDeviations[i]})
        result = {"standard_deviations": subresult}
        return result

    def combineMeanAndStandardDeviation(self, mean, sd):
        return self.toString(dict(mean.items() + sd.items()))

