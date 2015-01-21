from unittest import TestCase
import sys

import mock


# mock spark related modules for spark-unrelated unit tests
sys.modules["pyspark"] = mock.MagicMock()
sys.modules["pyspark.SparkContext"] = mock.MagicMock()
# mock unrelated modules
sys.modules["writer"] = mock.MagicMock()
sys.modules["writer.Writer"] = mock.MagicMock()

from src.q3_campaign_query_combi.test.mean_orders_per_campaign_query_combi import *


class TestMergeActions(TestCase):
    def setUp(self):
        self.u1 = {u'visit_id': 17633600156, u'uid': 68021018, u'campaign': 94, u'action': u'landed',
                   u'query': u'data science training'}
        self.u2 = {u'visit_id': 17633600156, u'uid': 68021018, u'action': u'order'}
        self.m1 = {u'visit_id': 17633600156, u'uid': 68021018, u'campaign': 94, u'query': u'data science training',
                   u'action': [u'landed', u'order']}
        self.m2 = {u'visit_id': 17633600156, u'uid': 68021018, u'campaign': 94, u'query': u'data science training',
                   u'action': [u'adclick', u'signup']}

    def test_two_unmerged_docs(self):
        result = mergeActions(self.u1, self.u2)
        assert result == {u'visit_id': 17633600156, u'uid': 68021018, u'campaign': 94,
                          u'query': u'data science training',
                          u'action': [u'landed', u'order']}

    def test_switch_master_and_slave(self):
        result = mergeActions(self.u2, self.u1)
        assert result == {u'visit_id': 17633600156, u'uid': 68021018, u'campaign': 94,
                          u'query': u'data science training',
                          u'action': [u'landed', u'order']}

    def test_one_merged_doc(self):
        result = mergeActions(self.m1, self.u2)
        assert result == {u'visit_id': 17633600156, u'uid': 68021018, u'campaign': 94,
                          u'query': u'data science training',
                          u'action': [u'landed', u'order', u'order']}

    def test_two_merged_docs(self):
        result = mergeActions(self.m1, self.m2)
        assert result == {u'visit_id': 17633600156, u'uid': 68021018, u'campaign': 94,
                          u'query': u'data science training',
                          u'action': [u'landed', u'order', u'adclick', u'signup']}


class TestDropUnusedKeys(TestCase):
    def test_keys_present(self):
        doc = {u'visit_id': 432288000, u'uid': 114594344, u'campaign': 558, u'tstamp': u'2014-09-15 00:21:13',
               u'experiments': [1, 4], u'action': u'landed', u'query': u'predictive modeling'}
        keys = [u'tstamp', u'experiments']
        result = dropUnusedKeys(doc, keys)
        assert result == {u'visit_id': 432288000, u'uid': 114594344, u'campaign': 558,
                          u'action': u'landed', u'query': u'predictive modeling'}

    def test_keys_missing(self):
        doc = {u'visit_id': 432288000, u'uid': 114594344, u'campaign': 558,
               u'action': u'landed', u'query': u'predictive modeling'}
        keys = [u'tstamp', u'experiments']
        result = dropUnusedKeys(doc, keys)
        assert result == {u'visit_id': 432288000, u'uid': 114594344, u'campaign': 558,
                          u'action': u'landed', u'query': u'predictive modeling'}


class TestGetValueAsList(TestCase):
    def setUp(self):
        self.doc = {u'action': [u'landed', u'adclick', u'adclick'], u'query': u'data science training',
                    u'visit_id': 52337976521, u'uid': 194966069, u'campaign': 127}

    def test_list_input(self):
        assert getValueAsList(self.doc, u'action') == [u'landed', u'adclick', u'adclick']

    def test_value_input(self):
        assert getValueAsList(self.doc, u'uid')


class TestGetListValuesFromDocs(TestCase):
    def setUp(self):
        self.u1 = {u'action': u'landed', u'query': u'data science training', u'visit_id': 17633600156, u'uid': 68021018,
                   u'campaign': 94}
        self.u2 = {u'action': [u'landed', u'adclick', u'adclick'], u'query': u'data science training',
                   u'visit_id': 52337976521, u'uid': 194966069, u'campaign': 127}
        self.m1 = {u'action': [u'landed', u'adclick', u'adclick'], u'query': u'data science training',
                   u'visit_id': 52337976521, u'uid': [118680467, 107807201], u'campaign': 127}
        self.m2 = {u'action': [u'landed', u'adclick', u'adclick'], u'query': u'data science training',
                   u'visit_id': 52337976521, u'uid': [196501891, 6356762], u'campaign': 127}

    def test_two_unmerged_docs(self):
        result = getListValuesFromDocs(self.u1, self.u2, u'uid')
        assert result == [68021018, 194966069]

    def test_two_merged_docs(self):
        result = getListValuesFromDocs(self.m1, self.m2, u'uid')
        assert result == [118680467, 107807201, 196501891, 6356762]

    def test_one_merged_one_unmerged_docs(self):
        result = getListValuesFromDocs(self.u1, self.m1, u'uid')
        assert result == [68021018, 118680467, 107807201]


class TestCombineUidsAndCountOrders(TestCase):
    def setUp(self):
        self.u1 = {u'action': u'landed', u'query': u'data science training', u'visit_id': 17633600156, u'uid': 68021018,
                   u'campaign': 127}
        self.u2 = {u'action': [u'landed', u'order', u'adclick'], u'query': u'data science training',
                   u'visit_id': 52337976521, u'uid': 194966069, u'campaign': 127}
        self.m1 = {u'campaign': 127, u'query': u'data science training', u'action': [u'order'],
                   u'uid': [68021018, 194966069], u'nbOrders': 1}
        self.m2 = {u'campaign': 127, u'query': u'data science training', u'action': [],
                   u'uid': [10797065, 25693103], u'nbOrders': 0}
        self.m3 = {u'campaign': 127, u'query': u'data science training', u'action': [u'order', u'order'],
                   u'uid': [10797065, 25693103], u'nbOrders': 2}

    def test_two_untreated_docs(self):
        result = combineUidsAndCountOrders(self.u1, self.u2)
        assert result == {u'campaign': 127, u'query': u'data science training', u'action': [u'order'],
                          u'uid': [68021018, 194966069], u'nbOrders': 1}

    def test_two_treated_docs(self):
        result = combineUidsAndCountOrders(self.m1, self.m2)
        assert result == {u'campaign': 127, u'query': u'data science training', u'action': [u'order'],
                          u'uid': [68021018, 194966069, 10797065, 25693103], u'nbOrders': 1}

    def test_one_treated_one_untreated_doc_without_orders(self):
        result = combineUidsAndCountOrders(self.m2, self.u1)
        print(result)
        assert result == {u'campaign': 127, u'query': u'data science training', u'action': [],
                          u'uid': [10797065, 25693103, 68021018], u'nbOrders': 0}

    def test_one_treated_one_untreated_doc(self):
        result = combineUidsAndCountOrders(self.m3, self.u1)
        print(result)
        assert result == {u'campaign': 127, u'query': u'data science training', u'action': [u'order', u'order'],
                          u'uid': [10797065, 25693103, 68021018], u'nbOrders': 2}


class TestCalculateMeanOrderPerVisitor(TestCase):
    def test_all_good(self):
        doc = {u'action': [u'order', u'order', u'order'], u'query': u'building predictive models', u'nbOrders': 3,
               u'uid': [88149732, 107807201, 71319366, 136664648, 46205578, 176121392, 182827314, 90999298, 155866558,
                        28710646, 56451281, 28602257, 187993104, 52254755, 115691073, 77684783, 46003261, 70651778,
                        65117887, 68619269, 34718784, 21087975, 177748044, 158348126, 122612324, 76046435, 71935200,
                        35906704, 99926314, 60484232, 54917736, 178321955, 78630255, 67818128, 25876035, 103062714,
                        49171888, 51359778, 44933876, 2159703, 161064818, 73703962, 80925431, 191914856, 104472473,
                        5454398, 181434244, 167617906, 151201097, 53262452, 50442557, 125548062, 41395146, 61391772,
                        85737475, 76371037], u'campaign': 203}
        result = calculateMeanOrderPerVisitor(doc)
        assert result == {u'campaign': 203, u'query': u'building predictive models', u'meanOrdersPerVisitor': 3/float(56)}