"""
An implementation of elementary cellular automaton with adjustable neighbourhood and number of possible states.
Inspired by https://matplotlib.org/matplotblog/posts/elementary-cellular-automata/.
"""

import numpy as np, matplotlib.pyplot as plt, sys

# Default values for a number of states and number of neighbours
BASE, NNEIGH = 3, 1

def rule_index(multiplet: list, base: int):
    """Computes an index assigned by a rule."""
    return int((base**3-1)-np.sum([base**(len(multiplet)-1-i)*x for (i,x) in enumerate(multiplet)]))

def cell_automaton(initial_state: list, n_itr: int, rule_num: int, base=BASE,nneigh=NNEIGH):
    """Evaluate evolution of an elementary cellular automaton.

    Parameters
    ----------
    initial_state: array-like Initial state of the automaton 
    n_itr: int Number of iterations of evolution
    rule_num: int A rule to be used, following Wolfram naming convention
    base: int,optional Number of states for the cells. The default is 3
    nneigh: int,optional Number of neighbours from each side for a single cell that constitute 'neighbourhood'. The default is 1.

    Returns
    -------
    CA_run: numpy.ndarray m*n_itr grid, where m is the size of the automaton, rows represent steps of evolution.

    """
    # check if provided rule exceeds the maximum value for a given base
    if rule_num<0 or np.log(rule_num)>(base**3*np.log(base)):
        raise ValueError(f"Invalid rule for base {base}.")
    # number of all possible inputs for the evolution function
    n_pos = base**(nneigh*2+1)
    # conversion of the rule number to a given base
    rule = np.zeros(n_pos)
    str_rule = np.fromiter(np.base_repr(rule_num,base=base),dtype=int)
    rule[n_pos-len(str_rule):] = str_rule

    m = len(initial_state)
    # a valiable containing all states of the automaton
    CA_run = np.zeros((n_itr, m))
    CA_run[0, :] = initial_state

    for i in range(1, n_itr):
        all_multiplets = np.stack([np.roll(CA_run[i-1,:],j) for j in range(-nneigh,nneigh+1)])
        CA_run[i, :] = rule[np.apply_along_axis(rule_index, 0, all_multiplets,base=base)]
    return CA_run

if __name__ == "__main__":
    
    argv = sys.argv[1:]
    init_state, n_itr, rule = argv[:3]
    rule = int(rule)
    n_itr = int(n_itr)
    init_state = np.fromiter(init_state,dtype=int)
    u_base, u_nneigh = None, None
    if len(argv)>3:
        u_base = int(argv[3])
        if len(argv)>4:
            u_nneigh = int(argv[4])

    base = u_base if u_base else BASE
    nneigh = u_nneigh if u_nneigh else NNEIGH

    cells = cell_automaton(init_state,n_itr,rule,base,nneigh)
    
    fig, ax = plt.subplots()
    ax.matshow(cells)
    ax.set_title(f"""Cellular automaton evolution ({n_itr} steps), 
        rule No. {rule}, 
        No. of states: {base}, neighbourhood: {2*nneigh}.
        """)
    ax.axis(False)
    plt.tight_layout()
    plt.show()