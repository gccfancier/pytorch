from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from caffe2.python import core, workspace
from caffe2.python.test_util import TestCase
import numpy as np


class TestPutOps(TestCase):

    def test_avg_put_ops(self):
        put_value = 15.1111
        magnitude_expand = 10000
        stat_name = "a1".encode('ascii')
        sum_postfix = "/stat_value/sum".encode("ascii")
        count_postfix = "/stat_value/count".encode("ascii")

        workspace.FeedBlob("value", np.array([put_value], dtype=np.float))

        workspace.RunOperatorOnce(core.CreateOperator(
            "AveragePut",
            "value",
            [],
            stat_name=stat_name,
            magnitude_expand=magnitude_expand))

        workspace.RunOperatorOnce(core.CreateOperator(
            'StatRegistryExport', [], ['k', 'v', 't']))

        k = workspace.FetchBlob('k')
        v = workspace.FetchBlob('v')

        stat_dict = dict(zip(k, v))

        self.assertIn(stat_name + sum_postfix, stat_dict)
        self.assertIn(stat_name + count_postfix, stat_dict)
        self.assertEquals(stat_dict[stat_name + sum_postfix],
         put_value * magnitude_expand)
        self.assertEquals(stat_dict[stat_name + count_postfix], 1)

    def test_increment_put_ops(self):
        put_value = 15.1111
        magnitude_expand = 10000
        stat_name = "i1".encode('ascii')
        member_postfix = "/stat_value".encode("ascii")

        workspace.FeedBlob("value", np.array([put_value], dtype=np.float))

        workspace.RunOperatorOnce(core.CreateOperator(
            "IncrementPut",
            "value",
            [],
            stat_name=stat_name,
            magnitude_expand=magnitude_expand))

        workspace.RunOperatorOnce(core.CreateOperator(
            'StatRegistryExport', [], ['k', 'v', 't']))

        k = workspace.FetchBlob('k')
        v = workspace.FetchBlob('v')

        stat_dict = dict(zip(k, v))

        self.assertIn(stat_name + member_postfix, stat_dict)
        self.assertEquals(stat_dict[stat_name + member_postfix],
         put_value * magnitude_expand)

    def test_stddev_put_ops(self):
        put_value = 15.1111
        magnitude_expand = 10000
        stat_name = "s1".encode('ascii')
        sum_postfix = "/stat_value/sum".encode("ascii")
        count_postfix = "/stat_value/count".encode("ascii")
        sumoffset_postfix = "/stat_value/sumoffset".encode("ascii")
        sumsqoffset_postfix = "/stat_value/sumsqoffset".encode("ascii")

        workspace.FeedBlob("value", np.array([put_value], dtype=np.float))

        workspace.RunOperatorOnce(core.CreateOperator(
            "StdDevPut",
            "value",
            [],
            stat_name=stat_name,
            magnitude_expand=magnitude_expand))

        workspace.RunOperatorOnce(core.CreateOperator(
            'StatRegistryExport', [], ['k', 'v', 't']))

        k = workspace.FetchBlob('k')
        v = workspace.FetchBlob('v')

        stat_dict = dict(zip(k, v))

        self.assertIn(stat_name + sum_postfix, stat_dict)
        self.assertIn(stat_name + count_postfix, stat_dict)
        self.assertIn(stat_name + sumoffset_postfix, stat_dict)
        self.assertIn(stat_name + sumsqoffset_postfix, stat_dict)
        self.assertEquals(stat_dict[stat_name + sum_postfix],
            put_value * magnitude_expand)
        self.assertEquals(stat_dict[stat_name + count_postfix], 1)
