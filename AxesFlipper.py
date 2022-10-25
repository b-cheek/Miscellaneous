##vals = ''
##print("Copy and paste the data from the spreadsheet here:")
##for i in range(0, 10):
##    vals += input() + "\n"
##
##arr = []
##for i in vals.split('\n'): arr.append(i)
##for i in range (0, len(arr)):
##	arr[i] = arr[i].split("\t")
##
##xVals = []
##for i in range(0, len(arr)):
##	for j in range(1, len(arr[i])):
##		if arr[i][j] not in xVals:
##			xVals.append(arr[i][j])
##
##for i in range(0, len(xVals)):
##	xVals[i] = [xVals[i], '', '', '']
##
##for i in range(0, len(arr)):
##	for j in range(1, len(arr[i])):
##		for k in range(0, len(xVals)):
##			if xVals[k][0]==arr[i][j]:
##				xVals[k][j]=arr[i][0]
##
##for i in xVals:
##	for j in i: print(j, end='\t')
##	print('')

print("Copy and paste the data from the spreadsheet here:")
arr = []
for i in range(0, 10):
    arr.append(input().split('\t'))

newArr = []
for i in arr:
    for j in range(1, len(i)):
        if i[j] not in newArr: newArr.append(i[j])

newArr = list(map(lambda xVal: [xVal, '', '', ''], newArr))

for i in range(0, len(arr)):
	for j in range(1, len(arr[i])):
		for k in range(0, len(newArr)):
			if newArr[k][0]==arr[i][j]:
				newArr[k][j]=arr[i][0]

for i in newArr:
	for j in i: print(j, end='\t')
	print('')
