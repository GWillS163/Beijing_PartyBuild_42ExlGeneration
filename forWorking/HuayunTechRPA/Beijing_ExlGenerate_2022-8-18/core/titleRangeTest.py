# -*- coding:utf-8 -*-

import unittest


# from shtOperation import getSht2IndexScp4Depart

def getColLtr(colNum: int) -> str:
    """0 -> A, 1 -> B, 2 -> C, ..., 26->AA, ..., 311 -> KZ
    :param colNum: the Column number of the Column Letter of Excel mappings
    :return the letter of Excel column
    """
    if colNum < 26:
        return chr(colNum + 65)
    else:
        return getColLtr(colNum // 26 - 1) + getColLtr(colNum % 26)


def getColNum(colLtr: str) -> int:
    """A -> 0, B -> 1, C -> 2, ..., AA->26, ..., KZ -> 311
    :param colLtr: the Column Letter of Excel
    :return the sequence number of Excel column
    """
    if len(colLtr) == 1:
        return ord(colLtr) - 65
    else:
        return (ord(colLtr[0]) - 64) * 26 + getColNum(colLtr[1:])

import re
def getSht2IndexScp4Depart(useAddress):
    """
    获取 sht2 中的部门数据的范围, 并+1
    :param useAddress: F1: KY3
    :return:F1: KZ3
    """
    # get the range of sht2
    sht2IndexScp = useAddress.split(":")
    # get the col of sht2
    sht2ColStr = re.findall(r"[A-Z]+", sht2IndexScp[1])[0]
    sht2RowStr = re.findall(r"\d+", sht2IndexScp[1])[0]
    sht2ColNew = getColLtr(getColNum(sht2ColStr) + 1)
    sht2IndexScp = f"{sht2IndexScp[0]}:{sht2ColNew}{sht2RowStr}"
    return sht2IndexScp


class titleRangeTest(unittest.TestCase):
    def test_turnTitleRange(self):
        res = getSht2IndexScp4Depart("D1:KY2")
        self.assertEqual("D1:KZ2", res)  # add assertion here


if __name__ == '__main__':
    unittest.main()
