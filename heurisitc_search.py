from collections import defaultdict
'''Author : Aditya Mayank Shankar'''
'''References:-'''
'''https://stackoverflow.com/questions/9139897/how-to-set-default-value-to-all-keys-of-a-dict-object-in-python'''
'''https://en.wikipedia.org/wiki/A*_search_algorithm'''


def solve(l1):
    expanded = []                       # List of values visited
    to_expand = list()                  # list of values that can be expanded
    to_expand.append(0)                 # 1st element to expand is 0
    parent = {}                         # Map that stores the parent nodes
    func_gn = defaultdict(lambda: 10000)  # g(n) function that tells cost in reaching from starting node
    func_gn.update({0: 0})              # cost of reacing 0 from starting(0) is 0
    func_fn = defaultdict(lambda: 10000)  # f(n) that would store the complete heuristic values
    func_fn.update({0: len(l1)-1})
    sol_path = []
    sol_string = ""

    while 1:
        values = {}                     # Map that stores heuristics for nodes in to_expand
        for node in to_expand:
            values.update({node: func_fn[node]})
        
        if bool(values) is False:       # If we run out of values in to_expand then it's unsolvable
            sol_string = 'No Solution'
            break
        
        current = get_min(values)
        upper = current + l1.__getitem__(current)  # upper and lower are the next candidates for expansion
        lower = current - l1.__getitem__(current)

        if upper == len(l1) - 1:        # If we reach the goal we will exit from loop
            parent[upper] = current
            sol_path = generatepath(parent, upper)  # calling path calculation function
            break
        
        to_expand.remove(current)               # Removing current from to_expand and adding to expanded
        expanded.append(current)

        if lower == 0 and upper == 0:           # Additional validations around invalid cases
            sol_string = 'No Solution'
            break
            
        for nextvalue in [upper, lower]:
            if 0 < nextvalue < len(l1)-1:       # Validations for out of bound values
                if nextvalue in expanded:
                    continue
                if nextvalue not in to_expand:
                    to_expand.append(nextvalue)
                    # temp_func_gn stores the temporary values for current nodes
                temp_func_gn = func_gn[current] + nextvalue-current

                if temp_func_gn > func_gn[nextvalue] or temp_func_gn == func_gn[nextvalue]:
                    continue
                # If the heuristic for new node is less then save it for  further expansion
                parent[nextvalue] = current                 # Storing in parent to compute path in the end
                func_gn[nextvalue] = temp_func_gn           # Storing heuristic values to determine next expansion
                func_fn[nextvalue] = func_gn[nextvalue]+heuristic(nextvalue, current, l1)  # f(n)=g(n)+h(n)

    sol_path.reverse()                      # Reversing order of insertion to compute path

    for i in range(0, len(sol_path)-1):     # Traversing through the path array to generate string
        if sol_path[i] < sol_path[i+1]:
            sol_string = sol_string+sol_string.join('R')
        else:
            sol_string = sol_string+sol_string.join('L')
    return sol_string


def generatepath(parent, current):      # Function that generates path by traversing the parent map
    total_path = list()
    total_path.append(current)
    while current in parent.keys():
        current = parent.get(current)
        total_path.append(current)
    return total_path


def heuristic(nextvalue, current, l1):  # Heuristic function calculating effort from current and to goal
    return abs(current - nextvalue) + len(l1) - 1 - nextvalue


def get_min(values):                    # Function to return key with minimum value
    return min(values, key=values.get)

