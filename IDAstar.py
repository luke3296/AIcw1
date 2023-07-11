'''
moves   18
yields  1349
time    0.0554659366607666

moves   22
yields  7884
time    0.26531124114990234

moves   24
yields  18045
time    0.5222156047821045

moves   26
yields  112185
time    3.104912757873535

moves   20
yields  3274
time    0.09406709671020508

moves   20
yields  339
time    0.012483358383178711

moves   14
yields  93
time    0.003516674041748047

moves   24
yields  14506
time    0.40217161178588867

moves   22
yields  12483
time    0.32170796394348145

moves   31
yields  168408
time    4.307790040969849
'''

import copy
import time

# global variable to count the number of yields called in the move_blank function
yields = 0

problems1 = [
    [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]],
    [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]],
    [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]],
    [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]],
    [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]]
]
g1 = [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]

problems2 = [
    [0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]],
    [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]],
    [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]],
    [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]],
    [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]],
]
g2 = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]


# generates the black tiles new row,col idx after a move up,down,left,right
def move_blank(i, j, n):
    global yields
    if i + 1 < n:
        yields = yields + 1
        yield (i + 1, j) #Move Down
    if i - 1 >= 0:
        yields = yields + 1
        yield (i - 1, j) #Move Up
    if j + 1 < n:
        yields = yields + 1
        yield (i, j + 1) # Move right
    if j - 1 >= 0:
        yields = yields + 1
        yield (i, j - 1) #Move Left


def move(state):
    # global yields
    [i, j, grid] = state
    n = len(grid)
    for pos in move_blank(i, j, n):
        i1, j1 = pos
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]
        # yields = yields + 1
        yield [i1, j1, grid]
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]


def getManhattan(cd, gd):
    (a, b, cs) = cd
    (c, d, gs) = gd
    distance = 0
    # for each element of the current state
    for i in range(len(cs)):
        for j in range(len(cs[i])):
            # if the element is misplaced
            if cs[i][j] != gs[i][j]:
                # for each element in the goal state, for each misplaced tile in the current state
                for k in range(len(gs)):
                    for l in range(len(gs[k])):
                        # i,j = row,col of the current state and k,l = row,col of the goal state
                        if cs[i][j] == gs[k][l]:
                            # sum the differences between the current states
                            # and the goal states row indexes and col indexes
                            distance = distance + abs(i - k) + abs(j - l)
    return distance


def depthLimtedAstar(path, g, depth, goal):
    """
    :param path: [ initialState ] (for the 3-puzzle where initialState is
                 [int,int,[[int,int,int],[int,int,int],[int,int,int]]] )
    :param g: int (The depth of the last state in path with respect to the initalState)
    :param depth:
    :param goal: [ [int,int,[[int,int,int],[int,int,int],[int,int,int]]] ] for the 3-puzzle first elem
                 is initialState and last elem is goal
    :return:
    """
    currentNode = path[-1]
    # get the f val which is the sum of heurist and depth
    f = g + getManhattan(currentNode, goal)
    # if the f score is
    if f > depth:
        return f
    if currentNode == goal:
        return True
    #biggest possible value for a number in python, acts as upper bound for
    #finding the smallest f value for successor states
    smallestF = float("inf")
    # nextState is a deep copy of the generated successor
    for successor in move(copy.deepcopy(currentNode)):
        # avoid looping by not expanding the same state twice
        if successor not in path:
            #append the succsessor to the end of path
            path.append(successor)
            # recursive call depth limited a star. Result is either
            result = depthLimtedAstar(path, g + 1, depth, goal)
            # the successor is the goal
            if result is True:
                return True
            #set smallestF to the smallest f value for successor states
            if result < smallestF:
                smallestF = result
            path.pop()
    #return the smallest f value for the successor states which will act as
    #the new depth to search to with a-star
    return smallestF


def ida_star(path1, goal):
    """
    :param path1:[ [int,int,[[int,int,int],[int,int,int],[int,int,int]]] ] (for the 3-puzzle)
    :param goal: [int,int,[[int,int,int],[int,int,int],[int,int,int]]]  (goal state for the 3-puzzle)
    :return: [ [int,int,[[int,int,int],[int,int,int],[int,int,int]]] ] for the 3-puzzle first elem
             is initialState and last elem is goal
    """
    # get the depth to go up to for the initialState
    depth = getManhattan(path1[-1], goal)
    while True:
        result = depthLimtedAstar(path1, 0, depth, goal)
        if result is True:
            return path1
            break
        # if there were no moves that generated a state with a cost < infinity wrt the initialState
        if result is float("inf"):
            print("no sol founds")
            break
        # set depth to the new f value
        depth = result


for problem in problems1:
    yields = 0
    start_time = time.time()
    path = ida_star([problem], g1)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("moves  ", len(path) - 1)
    print("yields ", yields)
    print("time   ", elapsed_time)
    print()

for problem in problems2:
    yields = 0
    start_time = time.time()
    path = ida_star([problem], g2)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("moves  ", len(path) - 1)
    print("yields ", yields)
    print("time   ", elapsed_time)
    print()

'''
#Q2 alternative move func
def move(state):
    [i, j, grid] = state
    n = len(grid)
    for pos in move_blank(i, j, n):
        i1, j1 = pos
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]
        yield [i1, j1, grid]
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]
    #store copoy of grid to restore later, this is ineffichent

    grid1 = copy.deepcopy(grid)
    #yield shift up
    beg =grid[0]
    for i in range(0,n-1,1):
        grid[i] = grid[i+1]
    grid[n-1] = beg
    #note this only works when the 0 tile is not in row 0; in this case i shoul be n-1
    if i != 0:
        yield [i+1,j, grid]
    else:
        yield [n-1,j, grid]

    #restore the orignal grid
    grid=grid1
    
    #yield shift down 
    end = grid[n-1]
    for i in range(n-1,0,-1):
        grid[i] = grid[i-1]
    grid[0] = end
    #note this only works when the 0 tile is not in row n-1; in this case i shoul be 0
    if i != n-1:
        yield [i - 1, j, grid]
    else:
        yield [0,j, grid]
'''