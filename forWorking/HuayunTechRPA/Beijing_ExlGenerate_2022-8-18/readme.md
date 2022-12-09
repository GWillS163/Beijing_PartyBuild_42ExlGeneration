# 项目介绍
代码逻辑：
- 读取文件 
- 分数判断 
- 数据计算
- 数据填写 （1个主表）
- 数据复制 （41个子表）

## 项目结构
```bash
CombineOutPut # Pycombiner 生成的文件夹
core # 核心代码
origin # 原始数据
release # 放置到RPA中的版本
test # 测试代码
realTest.py # 主程序入口
```
## 核心代码
 ```bash
 BEIJING_EXLGENERATE_2022-8-18\CORE
│  addPartitions.py
│  config.py
│  debugPrint.py
│  getScoreData.py  # 350行
│  main.py  # 入口程序 480行代码
│  scoreJudgeCore.py  # 答题判分模块 180行
│  shtDataCalc.py   # Sheet内数据计算 850行
│  shtOperation.py  # Sheet内单元格操作 450行 为操作excel的模块, 放置数据，修改格式等
│  userParamsProcess.py  # 用户参数处理 250行
│  utils.py  # 公共函数的模块
│  __init__.py
```

# 项目构建工具
由于开发复杂，为此构建了一个脚手架。

## 📦一键安装
```bash
pip install pycombiner # 需已安装Python3+
```
## ✨使用效果
命令行输入`pycombiner <入口文件>`执行。
得到了如下提示:
```bash
..Beijing_PartyBuild_42ExlGeneration>pycombiner .\test\realTest.py

        ------restImports------
import os
import re
import csv
import time
import datetime
import xlwings as xw
from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Optional
        ------restImports------
number of import line: 11
number of code lines: 2872

The output file is: .\CombineOutput\realTest20221209_125032.py
```
可以看到本项目汇总后 **共2800 行代码**， 且输出文件已保存至当前目录的`.\CombineOutput\`目录下。

### 🎉在RPA中使用
直接复制`.\CombineOutput\realTest20221209_125032.py` 的文件内容，粘贴至RPA中。 

 
