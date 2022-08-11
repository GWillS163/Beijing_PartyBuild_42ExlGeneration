#  Author : Github: @GWillS163

#  Time: $(Date)

# Author : Github: @GWillS163
# Time: $(Date)
import time
import random


# define a function to solve the stock buy & sell question
def stock_question_2(stock_price_list):
    max_profit = 0
    min_price = stock_price_list[0]
    for i in range(1, len(stock_price_list)):
        if stock_price_list[i] < min_price:
            min_price = stock_price_list[i]
        elif stock_price_list[i] - min_price > max_profit:
            max_profit = stock_price_list[i] - min_price
    return max_profit


if __name__ == '__main__':
    # tese the function 2
    stock_price_list = [7, 1, 5, 3, 6, 4]
    print(stock_question_2(stock_price_list))