
def pprint(text, n):
    if n<=0:
        return
    pprint(text, n-1)
    print(n, text)

pprint('233', 5)

# def sum_number(n):
#     if n <= 0:
#         return 0
#     return n+sum_number(n-1)
#
# print(sum_number(100))

