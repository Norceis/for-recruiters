import random
import matplotlib.pyplot as plt
import time


cities = 10 #number of cities
listofcities = []
letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z')
ifBroken = 1 #1 if only 80% connections are to exist
ifHeight = 1 #1 if roads to higher places are to be 10% longer and roads to lower places are to be 10% shorter

def coordinates():
    return [random.randint(-100, 100), random.randint(-100, 100), random.randint(0, 50)]

listofcities = [[letters[i], coordinates()] for i in range(0, cities)]
listofcoords = [listofcities[i][1] for i in range(0,len(listofcities))]
dictionaryofcoords = {}
for i in range(len(listofcities)):
    dictionaryofcoords[listofcities[i][0]] = listofcities[i][1]

def distance(x, y, ifHeight):
    if ifHeight:
        if y[2] > x[2]:
            return ((((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2 + (y[2] - x[2]) ** 2) ** (1 / 2))*0.9)
        elif y[2] == x[2]:
            return ((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2 + (y[2] - x[2]) ** 2) ** (1 / 2)
        else:
            return ((((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2 + (y[2] - x[2]) ** 2) ** (1 / 2))*1.1)
    else:
        return ((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2 + (y[2] - x[2]) ** 2) ** (1 / 2)

def matrixgenerator(listofcities, ifBroken):
    matrix=[]
    for i in listofcities:
        row=[]
        for j in listofcities:
            if i==j:
                row.append(None)
            else:
                row.append(distance(i[1],j[1],ifHeight))
        matrix.append(row)
    if ifBroken:
        noroads = round((cities**2-cities)*0.2)
        while noroads != 0:
            a, b = random.randrange(0,cities), random.randrange(0,cities)
            if a == b:
                continue
            else:
                matrix[a][b] = None
                noroads -= 1
    # for i in matrix:
    #     print(i)
    return matrix

def plot(list, bestperm):
    xs, ys, zs = [], [], []
    dataforlines = []
    for i in range(len(list)):
        xs.append(list[i][0])
        ys.append(list[i][1])
        zs.append(list[i][2])
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs, ys, zs)
    for i in bestperm:
        dataforlines += [dictionaryofcoords.get(i)]
    for i in range(len(dataforlines) - 1):
        plt.plot([dataforlines[i][0], dataforlines[i + 1][0]],
                 [dataforlines[i][1], dataforlines[i + 1][1]],
                 [dataforlines[i][2], dataforlines[i + 1][2]])
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    plt.show()


def permutation(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    l = []
    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i + 1:]
        for p in permutation(remLst):
            l.append([m] + p)
    return l


varlistofcities=[]
permutationsraw=[]
permutations=[]
for i in range(0, cities):
    varlistofcities += letters[i]
for p in permutation(varlistofcities):
    permutationsraw.append(p)
for p in range(len(permutationsraw)):
    permutations.append(permutationsraw[p])
    permutations[p].append(permutationsraw[p][0])


def bruteforce(matrix, permutations):
    bestperm = []
    bestpath = 1000
    for i in range(len(permutations)):
        currentpath = 0
        for j in range(len(permutations[i]) - 1):
            currentperm = permutations[i]
            try:
                currentpath += matrix[letters.index(permutations[i][j])][letters.index(permutations[i][j + 1])]
            except TypeError:
                currentpath += 1000
                break
        if currentpath < bestpath:
            bestpath = currentpath
            bestperm = currentperm

    return bestperm, bestpath

matrix = matrixgenerator(listofcities, ifBroken)
bestperm, bestpath = bruteforce(matrix, permutations)
plot(listofcoords, bestperm)
print(f'Best path is {bestperm} with distance {round(bestpath,2)}.')
print(time.perf_counter())




