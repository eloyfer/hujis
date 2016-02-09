from math import sqrt as sqrt
from timeit import default_timer as timer
import copy

start = timer()

rows = 0
cols = 0

class CC:

    def __init__(self):
        self.top = 0
        self.bottom = 0
        self.left = 0
        self.right = 0
        self.vSet = set()

    def getTable(self):
        rows = self.bottom - self.top + 1
        cols = self.right - self.left + 1
        table = [[0 for j in range(cols)] for i in range(rows)]
        for elm in self.vSet:
            table[elm[0] - self.top][elm[1] - self.left] = 1
        return table

def printTable(table):
    for row in table:
        for cell in row:
            print(cell, end = ' ')
        print()

def inBounds(i, j):
    if i < 0 or j < 0 or i >=rows or j >= cols:
        return False
    return True

def tableFromCC(cc):
    table = [[0 for j in range(cols)] for i in range(rows)]
    for elm in cc:
        table[elm[0]][elm[1]] = 1
    return table


##fileName = "learn_and_teach"
fileName = "right_angle"
##fileName = "logo"
##fileName = "test"

f = open(fileName + ".in")

table = []

size = f.readline().split()
rows = int(size[0])
cols = int(size[1])
table = [[] for i in range(rows)]
i = 0
for line in f:
    #print("line" + str(i))
    for c in line:
        if c == '.':
            table[i].append(0)
        if c == '#':
            table[i].append(1)
    i += 1

f.close()

tableCopy = copy.deepcopy(table)

ccList = []

def getAdjacents(i,j):
    return [(i+1,j), (i-1,j), (i, j+1), (i, j-1)]

def addToCC(cc, i, j):
    stack = [(i,j)]
    while len(stack) > 0:
        v = stack.pop()
        if inBounds(v[0], v[1]) and table[v[0]][v[1]]:
            cc.add((v[0], v[1]))
            table[v[0]][v[1]] = 0
            stack = stack + getAdjacents(v[0], v[1])

def findCC():
    global rows
    global cols
    # find connected components
    for i in range(rows):
        for j in range(cols):
            if table[i][j]:
                cc = CC()
                addToCC(cc.vSet, i, j)
                ccList.append(cc)
                tmp = sorted(cc.vSet, key = lambda tup: tup[0])
                cc.top = tmp[0][0]
                cc.bottom = tmp[-1][0]
                tmp = sorted(cc.vSet, key = lambda tup: tup[1])
                cc.left = tmp[0][1]
                cc.right = tmp[-1][1]
            

findCC()

result = ''
commands = 0

def paintLine(r1, c1, r2, c2):
    global commands
    global result
    commands += 1
    result += "PAINT_LINE %d %d %d %d\n" % (r1, c1, r2, c2)

def paintSquare(r, c, s):
    global commands
    global result
    commands += 1
    result += "PAINT_SQUARE %d %d %d\n" % (r, c, s)

def eraseCell(r, c):
    global commands
    global result
    commands += 1
    result += "ERASE_CELL %d %d\n" % (r, c)
    

for cc in ccList:
    rows = cc.bottom - cc.top + 1
    cols = cc.right - cc.left + 1
    top = cc.top
    left = cc.left

    table = cc.getTable()

    # paint lines
    if rows < cols:
        for i in range(rows):
            count = 0
            for j in range(cols):
                if not table[i][j] and count:
                    paintLine(i + top, j + left - count, i + top, j + left - 1)
                    count = 0
                if table[i][j]:
                    count += 1
            if count:
                paintLine(i + top, j + left - count + 1, i + top, j + left)
    else:
        for j in range(cols):
            count = 0
            for i in range(rows):
                if not table[i][j] and count:
                    paintLine(i + top - count, j + left, i + top - 1, j + left)
                    count = 0
                if table[i][j]:
                    count += 1
            if count:
                paintLine(i + top - count + 1, j + left, i + top, j + left)
                

f = open(fileName + ".out" , 'w')
f.write(str(commands) + '\n' + result)
f.close()

end = timer()
print(end - start)
