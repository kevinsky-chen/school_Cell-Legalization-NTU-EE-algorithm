import numpy as np
import sys

INT_MAX = 10000
w = []         # each chip's width
x = []         # each chip's initial(optimal) position
e = []         # each chip's weight in the linear cost function
cw_l = []      # cumulative width from left side
cw_r = []      # cumulative width from right side
result_x = []  # save solution
#opt_c = np.zeros(shape=(2, W+1), dtype=int)
#opt_x = np.zeros((n+1,), dtype=int)


def cumulativeWidth(W, n, cw_l, cw_r):
    # calculating each cell's span
    left = 0
    right = W - w[n - 1]

    for i in range(n):
        cw_l.append(left)
        cw_r.append(right)
        left += w[i]
        right -= w[n - 2 - i]


def retrieveSolution(solution, initial_x, initial_y):
    y = initial_y
    x = initial_x

    while(x > 0 and y > 0):
        if(solution[y][x] > 0):  # toward bottom-right => toward top-left in backtracking
            x -= solution[y][x]
            y -= 1
            result_x.append(x)
        else:                   # toward right => toward left in backtracking
            x -= 1


if __name__ == '__main__':
    # ::: check validity :::
    if len(sys.argv) < 3:
        print('Please address your "Input File Name" and "Output File Name"')
        sys.exit()

    # ::: read input file :::
    f = open(sys.argv[1], "r")
    W = int(f.readline())    # the width of the row
    n = int(f.readline())    # the number of the cell to place in this row
    print("W= ", W, " ,n= ", n)
    for _w in (f.readline()).split():
        w.append(int(_w))
    for _x in (f.readline()).split():
        x.append(int(_x))
    for _e in (f.readline()).split():
        e.append(int(_e))
    f.close()

    # ::: initialize :::
    # negative->toward right; positive->toward bottom-right => -1->move toward right 1; +3->move toward bottom 1 and right 3
    opt_c = [[INT_MAX for i in range(W+1)] for j in range(2)]
    opt_x = [[-1 for i in range(W+1)] for j in range(n+1)]
    cumulativeWidth(W, n, cw_l, cw_r)

    # ::: Dynamic Programming :::
    for i in range(W+1):
        print("i: ", i)
        opt_c[0][i] = 0

    for j in range(1, n+1):
        for i in range(1, W+1):
            if (i <= cw_l[j - 1]):
                opt_c[1][i] = INT_MAX
                pass
            else:
                if (opt_c[0][i - w[j - 1]] + e[j - 1] * abs(i - w[j - 1] - x[j - 1]) < opt_c[1][i - 1]):
                    opt_c[1][i] = opt_c[0][i - w[j - 1]] + \
                        e[j - 1] * abs(i - w[j - 1] - x[j - 1])
                    #opt_x[j][i] = i - w[j - 1]
                    opt_x[j][i] = w[j - 1]
                else:
                    opt_c[1][i] = opt_c[1][i-1]
                    opt_x[j][i] = -1

        for i in range(W+1):
            opt_c[0][i] = opt_c[1][i]

    # ::: Print Output :::
    print("optimal solution's cost: ", opt_c[1][W])
    retrieveSolution(opt_x, W, n)
    result_x = list(map(str, reversed(result_x)))   # int->string
    with open(sys.argv[2], 'w') as f:
        f.write(str(opt_c[1][W]))   # optimal cost
        f.write('\n')
        f.write('\n'.join(result_x))
