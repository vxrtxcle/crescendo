# top mid left - 52, top mid - 51, top left - 53 bottom right = 50 bottom mid = 49-top mid right - 48 top right - 47 bottom left-42
import csv
from matplotlib import pyplot as plt
import urllib.request

count2 = 0
teamNumber = 0
allianceColor = ''
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]
bl, bm, br, tl, tml, tm, tmr, tr = [False,0], [False,0], [False,0], [False,0], [False,0], [False,0], [False,0], [False,0]
with open('Data Set.csv', 'r') as file:
   reader = csv.reader(file)
   for x in reader:
       count1 = 0
       count2 += 1
       for y in x:
           if (count1 == 9 and y != '') and count2 == 2:
               teamNumber = y
           if (count1 == 10 and y != '') and count2 == 2:
               allianceColor = y
           if (count1 == 42 and y != '') and count2 == 2:
               bl[0] = True
               print(bl[0])
               bl[1] = str(y)
           if (count1 == 47 and y != '') and count2 == 2:
               tr[0] = True
               print("Top Right")
               tr[1] = str(y)
           if (count1 == 48 and y != '') and count2 == 2:
               tmr[0] = True
               print("Top Middle Right")
               tmr[1] = str(y)
           if (count1 == 49 and y != '') and count2 == 2:
               bm[0] = True
               print("Bottom Middle")
               bm[1] = str(y)
           if (count1 == 50 and y != '') and count2 == 2:
               br[0] = True
               print("Bottom Right")
               br[1] = str(y)
           if (count1 == 51 and y != '') and count2 == 2:
               tm[0] = True
               print("Top Mid")
               tm[1] = str(y)
           if (count1 == 52 and y != '') and count2 == 2:
               tml[0] = True
               print(y)
               tml[1] = str(y)
           if (count1 == 53 and y != '') and count2 == 2:
               tl[0] = True
               print(y)
               tl[1] = str(y)
           count1 += 1
ArrayPath = [bl[0],bm[0],br[0],tl[0],tml[0],tm[0],tmr[0],tr[0]]
ArrayTimes = [bl[1], bm[1], br[1], tl[1], tm[1], tml[1], tmr[1], tr[1]]
print(ArrayTimes)
count1 = 0
for i in ArrayTimes:
    if i != 0:
        if '|' in i:
            j = i.split('|')
            print(j)
            j.pop()
            for x in j:
                ArrayTimes[count1] = x
                bm[1] = x
    count1 += 1
print(ArrayPath)
ArrayTimes = remove_values_from_list(ArrayTimes, 0)
ArrayTimes.sort()
print(ArrayTimes)
x, y = [], []
result = ''
for i in ArrayTimes:
    if i == bl[1]:
        result += "Bottom Left "
        x.append(2.5)
        y.append(3)
    elif i == bm[1]:
        result += "Bottom Mid "
        x.append(2.5)
        y.append(2.25)
    elif i == br[1]:
        result += "Bottom Right "
        x.append(2.5)
        y.append(1.5)
    elif i == tl[1]:
        result += "Top Left "
        x.append(5)
        y.append(4.6)
    elif i == tml[1]:
        result += "Top Mid Left "
        x.append(5)
        y.append(3.9)
    elif i == tm[1]:
        result += "Top Mid "
        x.append(5)
        y.append(3)
    elif i == tmr[1]:
        result += "Top Mid Right "
        x.append(5)
        y.append(2.3)
    elif i == tr[1]:
        result += "Top Right "
        x.append(5)
        y.append(1.6)
    else:
        result += ''
print(result)
img = plt.imread('field.jpg')
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(img, extent=[0, 10, 0, 6])
plt.grid()
plt.title("Team " + str(teamNumber))
plt.plot(x, y, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
plt.show()






