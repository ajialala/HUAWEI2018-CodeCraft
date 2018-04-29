import csv
import math
import random


def func():
    # csv_filename = '../code/traindata.csv'
    # test_filename = '../code/testdata.csv'
    csv_filename = 'traindata.csv'
    test_filename = 'testdata.csv'
    flavor = []
    month = []
    day = []
    week = []
    number = []
    ndat = 638
    odat = 210
    ncol = 5
    trsubset = zeros((ndat, ncol)).data

    # Loop over the data set
    with open(csv_filename, 'r') as csv_fh:

        reader = csv.reader(csv_fh)

        # Loop over the file by rows and fill in arrays for features
        for row in reader:
            flavor.append(float(row[0]))
            month.append(float(row[1]))
            day.append(float(row[2]))
            week.append(float(row[3]))
            number.append(float(row[4]))

    # Store the data as numpy array
    total = [flavor, month, day, week, number]
    flavor = array(flavor)
    month = array(month)
    day = array(day)
    week = array(week)
    number = array(number)

    ntree = 60
    mtry = 4
    mdepth = 30
    summ = [0.0 for i in range(odat)]
    # summ = 0

    # Aggregate and average the inidividual tree's regression prediction
    for x in range(1, ntree + 1):
        for y in range(0, ndat):
            # ran = np.random.randint(1, ndat)
            ran = random.randint(1, ndat - 1)
            for z in range(0, 5):
                trsubset[y][z] = total[z][ran]

        featsubset = []
        lst = [0, 1, 2, 3]
        for i in range(mtry):
            a = random.choice(lst)
            featsubset.append(a)
            lst.remove(a)

        # test = decisiontree(mdepth, trsubset, featsubset)

        def build(data, i):

            # optimal values to keep track of
            opt_infogain = 0.
            opt_cond = None
            opt_split = None
            var = variance(data)

            if len(data) == 0:
                return treenode()

            debugint = 0

            for x in featsubset:
                debugint += 1
                tempdat = {}

                for film in data:
                    tempdat[film[x]] = 0

                for val in tempdat:
                    (d1, d2) = binsplit(data, x, val)
                    p = float(len(d1)) / len(data)
                    infogain = var - (p * variance(d1) + (1 - p) * variance(d2))

                    if infogain > opt_infogain and len(d1) > 0 and len(d2) > 0:
                        opt_infogain = infogain
                        opt_cond = (x, val)
                        opt_split = (d1, d2)

            if opt_infogain > 0 and i < mdepth:
                return treenode(col=opt_cond[0], val=opt_cond[1], tnode=build(opt_split[0], i + 1),
                                fnode=build(opt_split[1], i + 1))
            else:
                return treenode(res=count(data))

        # Train the tree
        tree = build(trsubset, 0)

        # Use the trained tree to predict
        test = []
        oflavor = []
        omonth = []
        oday = []
        oweek = []

        # test_filename = '../code/testdata.csv'
        with open(test_filename, 'r') as csv_fh:
            reader = csv.reader(csv_fh)

            # Loop over the file by rows and fill in arrays for features
            for row in reader:
                oflavor.append(float(row[0]))
                omonth.append(float(row[1]))
                oday.append(float(row[2]))
                oweek.append(float(row[3]))

        for x in range(0, odat):
            test.append(predict([oflavor[x], omonth[x], oday[x], oweek[x]], tree))
        test = array(test)

        test = test.data
        summ = [test[i] + summ[i] for i in range(len(test))]
    prediction = [round(summ[i] / ntree) for i in range(len(summ))]

    preCount = {}
    flag = 0
    flavorCount = {}
    for fl in oflavor:
        if fl not in preCount.keys():
            preCount[fl] = 0
        preCount[fl] += prediction[flag]
        flag += 1
    result = {}
    for key,value in preCount.items():
        result['flavor'+str(int(key))] = value
    return result

class SimpleArray(object):
    def __init__(self):
        self.shape = []
        self.data = None

    def _ValidateShape(self, data, ind):
        if not isiterable(data):
            return
        if ind >= len(self.shape):
            self.shape.append(len(data))
        else:
            if self.shape[ind] != len(data):
                raise ValueError("Inconsistent shape")

        for val in data:
            self._ValidateShape(val, ind + 1)

def isiterable(data):
    try:
        chkit = iter(data)
    except TypeError, te:
        return False
    return True

def array(data):
    arr = SimpleArray()
    arr.shape = []
    if not isiterable(data):
        raise ValueError("Input must be iterable")
    arr._ValidateShape(data, 0)
    arr.data = [float(data[i]) for i in range(len(data))]
    arr.shape = tuple(arr.shape)
    return arr

def zeros(shape):
    arr = SimpleArray()
    arr.shape = tuple(shape)
    if not isiterable(shape):
        raise ValueError("Shape must be iterable")
    arr.data = []

    def GenData(shape, leafs):
        dim = shape.pop(0)
        newLeafs = []
        if len(shape) == 0:
            for l in leafs:
                for i in range(dim):
                    l.append(0.0)
        else:
            for l in leafs:
                for i in range(dim):
                    nl = []
                    l.append(nl)
                    newLeafs.append(nl)
            GenData(shape, newLeafs)

    GenData(list(arr.shape)[:], [arr.data])
    return arr

# def main():
#
#     ntree = 60
#     mtry = 4
#     mdepth = 30
#
#     prediction = randomforest(ntree, mtry, mdepth)
#     print(prediction)

# Create individual decision tree with the maximum depth md
# and the given subset of data and features
def decisiontree(md, dat, feature):
    # md : maximum depth of the tree
    # dat : data to put through the tree
    # feature : feature to split the data by in the nodes
    # Recursive function for constructing a decision tree
    def build(data, i):

        # optimal values to keep track of
        opt_infogain = 0.
        opt_cond = None
        opt_split = None
        var = variance(data)

        if len(data) == 0:
            return treenode()

        debugint = 0

        for x in feature:
            debugint += 1
            tempdat = {}

            for film in data:
                tempdat[film[x]] = 0

            for val in tempdat:
                (d1, d2) = binsplit(data, x, val)
                p = float(len(d1)) / len(data)
                infogain = var - (p * variance(d1) + (1 - p) * variance(d2))

                if infogain > opt_infogain and len(d1) > 0 and len(d2) > 0:
                    opt_infogain = infogain
                    opt_cond = (x, val)
                    opt_split = (d1, d2)

        if opt_infogain > 0 and i < md:
            return treenode(col=opt_cond[0], val=opt_cond[1], tnode=build(opt_split[0], i + 1),
                            fnode=build(opt_split[1], i + 1))
        else:
            return treenode(res=count(data))

    # Train the tree
    tree = build(dat, 0)

    # Use the trained tree to predict
    prediction = []
    oflavor = []
    omonth = []
    oday = []
    oweek = []

    test_filename = '../code/testdata.csv'
    with open(test_filename, 'r') as csv_fh:
        reader = csv.reader(csv_fh)

        # Loop over the file by rows and fill in arrays for features
        for row in reader:
            oflavor.append(float(row[0]))
            omonth.append(float(row[1]))
            oday.append(float(row[2]))
            oweek.append(float(row[3]))

    for x in range(0, odat):
        prediction.append(predict([oflavor[x], omonth[x], oday[x], oweek[x]], tree))
    prediction = array(prediction)
    return prediction

# Construct a random forest by aggregating B decision trees with
# Boostrapped data subset and random selection without replacement
# of the features
# def randomforest(B, mtry, mdepth):
#     # B : number of trees
#     # mtry : number of subset of features used for individual decision trees
#     # mdepth : maximum depth of decision trees
#
#     summ = [0.0 for i in range(odat)]
#     # summ = 0
#
#     # Aggregate and average the inidividual tree's regression prediction
#     for x in range(1, B + 1):
#         for y in range(0, ndat):
#             # ran = np.random.randint(1, ndat)
#             ran = random.randint(1, ndat - 1)
#             for z in range(0, 5):
#                 trsubset[y][z] = total[z][ran]
#
#         featsubset = []
#         lst = [0, 1, 2, 3]
#         for i in range(mtry):
#             a = random.choice(lst)
#             featsubset.append(a)
#             lst.remove(a)
#
#         test = decisiontree(mdepth, trsubset, featsubset)
#         test = test.data
#         summ = [test[i] + summ[i] for i in range(len(test))]
#     prediction = [round(summ[i] / B) for i in range(len(summ))]
#     return prediction

# Representation of tree as a decisionnode class;
class treenode:
    def __init__(self, col=-1, val=None, res=None, tnode=None, fnode=None):
        self.col = col
        self.val = val
        self.res = res
        self.tnode = tnode
        self.fnode = fnode

# A binary split of the data based on the value of val
def binsplit(data, col, val):
    # data : data to split
    # col : the column (feature) of the data to split by the value of
    # val : the value that determines the binary split

    splitfn = lambda row: row[col] >= val
    d1 = [row for row in data if splitfn(row)]
    d2 = [row for row in data if not splitfn(row)]
    return (d1, d2)

# Variance of the data
def variance(data):
    gross = []
    if len(data) == 0:
        return 0
    for row in data:
        gross.append(float(row[len(row) - 1]))
    # variance = sum([(i - (sum(gross)/len(gross)))**2 for i in gross])/len(gross)

    numEntries = len(gross)
    pool = {}
    for ele in gross:
        if ele not in pool.keys():
            pool[ele] = 0
        pool[ele] += 1
    variance = 0.0
    for key in pool:
        prob = float(pool[key]) / numEntries
        variance = variance - prob * math.log(prob, 2)

    return variance

# Count (unique) number of data
def count(data):
    count = {}
    for row in data:
        last = row[len(row) - 1]
        if last not in count:
            count[last] = 0
        count[last] += 1
    return count

# Given an input, follow the tree and average the values of resulting res
def predict(inp, tree):
    # inp : input features of a film to predict the ratings of
    # the decision tree to base the decision (prediction) on

    if tree.res != None:
        summ = 0
        num = 0
        for key in tree.res:
            summ += key * tree.res[key]
            num += tree.res[key]
        return summ / num
    else:
        v = inp[tree.col]
        branch = None
        if v >= tree.val:
            branch = tree.tnode
        else:
            branch = tree.fnode
        return predict(inp, branch)

