import json


class Writer:
    def __init__(self, outFile):
        self.outFile = outFile

    def writeOutputJson(self, bestMeanCampaignQuery, listOfStandardDeviations):
        bestMeanCampaignQuery[u'query_string'] = bestMeanCampaignQuery.pop(u'query')
        del (bestMeanCampaignQuery[u'meanOrdersPerVisitor'])
        # assert type(listOfStandardDeviations) == list and \
        # all([["campaign", "query_string", "standard_deviation"] == el.keys() for el in listOfStandardDeviations])
        result = json.dumps({"highest_mean_value": bestMeanCampaignQuery,
                             "standard_deviations": listOfStandardDeviations}, indent=True, sort_keys=True)
        of = open(self.outFile, "w+")
        of.write(result)
        of.close()