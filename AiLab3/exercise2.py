import math


class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)   # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''
def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_FIRST(fringe)
        print(node.STATE, GOAL_STATE)
        if node.STATE[0] == GOAL_STATE[0]:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''
def EXPAND(node):
    successors = []
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + child[2]
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''
def INSERT(node, queue):
    sucessorList = [node]
    for _node in queue:
        sucessorList.append(_node)
    return sucessorList

'''
Insert list of nodes into the fringe
'''

def INSERT_ALL(list, queue):
    for node in list:
        queue = INSERT(node, queue)
    return queue
'''
Removes and returns the first element from fringe
'''
def REMOVE_FIRST(queue):
    lowestValue = math.inf
    lowest = ""
    for node in queue:
        if node.STATE[1] + node.DEPTH < lowestValue:
            lowest = node
    print("lowest: {}".format(lowest))
    queue.remove(lowest)
    return lowest
'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state[0]]  # successor_fn( 'C' ) returns ['F', 'G']


INITIAL_STATE = ('A',6,2)
GOAL_STATE = ('K')
STATE_SPACE = {('A'): [('B',2,1), ('C',5,2),('D',2,4)],
               ('B'): [('F',5, 5), ('E',4,4)],
               ('C'): [('E',4,1)],
               ('D'): [('H',1, 1), ('I',2,4),('J',1,2)],
               ('E'): [('G',4, 2), ('H',1,2)],
               ('F'): [('G',4, 1)],
               ('G'): [('K',0, 6)],
               ('H'): [('K',0, 6), ('L',0,5)],
               ('I'): [('L', 0,3)],
               ('J'): [('J',math.inf,0)],
               ('L'): [('L',math.inf,0)],
               ('K'): [('K',0,0)]
               }


'''
Run tree search and display the nodes in the path to goal node
'''
def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
