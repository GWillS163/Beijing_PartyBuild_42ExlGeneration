sta = ''
staAvg = 'sum(sta)/len(sta)'
staAvgUnit = 'staAvg + staAvg'
staffWithLv = {"lv2_0": {"lv3_0": [sta, sta],
                         "lv3_1": [sta, sta]},
               "lv2_1": {"lv3_0": [sta, sta],
                         "lv3_1": [sta, sta]}
               }

sht1WithLv = {"lv2_0": {"lv3_0": [staAvg],
                        "lv3_1": [staAvg],
                        "二级单位": [staAvg]},
              "lv2_1": {"lv3_0": [staAvg],
                        "lv3_1": [staAvg],
                        "二级单位": [staAvg]},
              }

# 用的时候 需要 * weight
sht2WithLv = {"lv2_0": {"lv3_0": [staAvgUnit],
                        "lv3_1": [staAvgUnit],
                        "二级单位成绩": [],
                        "本线条排名": [],
                        "全公司排名": [],
                        },
              }


sht3WithLv = {"lv2_0": {"lv3_0": [staAvgUnit],