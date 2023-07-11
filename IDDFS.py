'''
moves   18
yields  231356
time    1.9746923446655273

moves   22
yields  2266109
time    20.905556201934814

moves   24
yields  6469723
time    71.6753511428833

moves   26
yields  25176830
time    261.1092686653137

moves   20
yields  561396
time    6.347639560699463

moves   20
yields  692005
time    8.04245901107788

moves   14
yields  18570
time    0.15827250480651855

moves   24
yields  4737798
time    48.33743119239807

moves   22
yields  1558399
time    14.9317045211792

moves   31
yields  221466957
time    2032.2597062587738
'''

import copy
import time

# global varible to count the number of yields
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
    [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
]
g2 = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]


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
        yield ([i1, j1, grid])
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]


# recursive depth limited search
def dls_rec(path1, depth, goal):
    """
    :param path1:[ initialState ] (for the 3-puzzle where initialState is  [int,int,[[int,int,int],[int,int,int],[int,int,int]]] )
    :param depth: int
    :param goal: [int,int,[[int,int,int],[int,int,int],[int,int,int]]]
    :return: [ [int,int,[[int,int,int],[int,int,int],[int,int,int]]] ] for 3 puzzle where 1st elem is inital state and last is goal state
    """
    # if the last element in the path is the goal return the path
    if goal == (path1[-1]):
        return path1
    # depth decreases from incrementing values of depth up to maxDepth in iddfs_rec to 0. if 0 no sol was found at iddfs_rec.maxDepth
    elif depth == 0:
        return None
    else:
        # nextState is a deep copy of the generated successor
        for nextState in move(copy.deepcopy(path1[-1])):
            # avoid looping by not expanding the same state twice
            if nextState not in path1:
                # make a new path with the successor appended to the end
                nextPath = (path1 + [nextState])
                # recursively call dls_rec with the successor nodes
                solution = dls_rec(nextPath, depth - 1, goal)
                #solution
                if solution is not None:
                    return solution
        return None


# iterative deepening dfs with a maxDepth limit
def iddfs_rec(path, maxDepth, goal):
    """
    :param path: [ initialState ] (for the 3-puzzle where initialState
                 is  [int,int,[[int,int,int],[int,int,int],[int,int,int]]] )
    :param maxDepth: int (specicfys the max depth iddfs will go up to)
    :param goal: [int,int[[int,int,int],[int,int,int],[int,int,int]]] (for the 3-puzzle)
    :return: [ [int,int,[[int,int,int],[int,int,int],[int,int,int]]] ]
               for the 3-puzzle first elem is initialState and last elem is goal
    """
    depth = 1
    while True:
        sol = dls_rec(path, depth, goal)
        # there was no solution found at the current depth
        if sol is None:
            # increment the search depth
            depth = depth + 1
            if depth == maxDepth:
                # break out of infinite loop is no solution was found within maxDepth
                return None
        # there was a solution found at the current depth
        else:
            return sol


for problem in problems1:
    # set yields global varible to 0 for each call of iddfs_rec
    yields = 0
    start_time = time.time()
    path = iddfs_rec([problem], 40, g1)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("moves  ", len(path) - 1)
    print("yields ", yields)
    print("time   ", elapsed_time)
    print()

for problem in problems2:
    # reset yields global yields varible to 0 for each call of iddfs_rec
    yields = 0
    start_time = time.time()
    path = iddfs_rec([problem], 40, g2)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("moves  ", len(path) - 1)
    print("yields ", yields)
    print("time   ", elapsed_time)
    print()
