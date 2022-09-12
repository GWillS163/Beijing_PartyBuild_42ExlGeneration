#!/bin/bash
# 本题为考试多行输入输出规范示例，无需提交，不计分。

read -r name number price
while [ "$name" ]
  do
    sum=$((number*price))
    printf "%s\t%s\t%s\t%s￥\n" "$name" "$number" "$price" "$sum"
    read -r name number price
  done
exit 0