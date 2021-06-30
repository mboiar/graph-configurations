'''
solve Sudoku puzzles with backtracking algorithm. 
(projecteuler.net, problem no. 96)
'''

import numpy as np, sys

def check(a, i, val):
    """
    Check if 'val' at position 'i' in 9x9 matrix 'a' satisfies sudoku rules.
    """
    i0=3*(i//3)
    mask=np.zeros((9,9))
    mask[i[0],:] = 1
    mask[:,i[1]]=1
    mask[i0[0]:i0[0]+3,i0[1]:i0[1]+3] = 1
    return np.all(a[mask==1]!=val)

def solve(a):
    """
    Uses backtracking to solve sudoku matrix 'a'. Returns True if solved successfully.
    """
    if a.all(): return True     # if no cell is empty, puzzle is solved
    i = np.argwhere(a==0)[0]
    for val in np.arange(1,10): # try each value and check conditions,
        if check(a,i,val):      # if satisfied, continue solving recursively
            a[i[0],i[1]] = val
            ok = solve(a)
            if ok: return True
            a[i[0],i[1]] = 0
    return False

if __name__ == '__main__':

    with open(sys.argv[1], 'r') as f:
        inp = f.readlines()
    raw = [''.join(inp[i:i+9]) for i in range(1,len(inp)+1,10)]
    res =[]
    for item in raw:
        a = np.array([list(map(int,i)) for i in item.strip().split('\n')],dtype=np.int64)
        solve(a)
        res.append(a)
    # ProjectEuler answer format
    res = sum([int(''.join([str(a[0,0]),str(a[0,1]),str(a[0,2])])) for a in res])
    print(res)
