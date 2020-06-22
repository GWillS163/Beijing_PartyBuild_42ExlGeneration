#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

color_list = [['r', '0.5', '0.5', '#FF00FF'], ['r', '0.2', '0.2', '#FF00FF']]

df = pd.DataFrame(np.random.randn(2, 4), columns=list('ABCD'))

ax.table(cellText=df.values,
         cellColours=color_list,
         colLabels=df.columns,
         loc='center')

fig.tight_layout()

plt.show()
