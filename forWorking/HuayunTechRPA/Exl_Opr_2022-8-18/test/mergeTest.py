#  Author : Github: @GWillS163
#  Time: $(Date)


from mainTest import *

sht, sht2_WithWeight = init()

deleteRowLst = [31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5]
for row in deleteRowLst:
    sht2_WithWeight.range(f"B{row}").api.EntireRow.Delete()
    # set the width of the B column to 290

print(sht2_WithWeight.range("B1:B2").column_width)
print(sht2_WithWeight.range("B1:B2").row_height)
sht2_WithWeight.range("B1").column_width = 18.8

# get merge cells scope dynamically
mergeCells = []
temp = None
n = 3
while True:
    if not sht2_WithWeight.range(f"B{n}").value:
        print(temp)
        mergeCells.append(temp)
        break
    if sht2_WithWeight.range(f"A{n}").value:
        if temp:
            print(temp)
            mergeCells.append(temp)
        print(f"A{n}")
        mergeCells.append(f"A{n}")
    else:
        temp = f"A{n}^^"
    n += 1

# show the merged cells gradually with step 2
for i in range(0, len(mergeCells), 2):
    print(mergeCells[i:i+2])
    # sht2_WithWeight.range(mergeCells[i:i+2]).merge()


