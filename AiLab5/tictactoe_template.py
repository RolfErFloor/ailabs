
def minmax_decision(state):
    infinity = float('inf')

    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        #print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


def is_terminal(state):
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    for (y) in range(3):
        if state[y] == state[y+3] == state[y+6]:
            return True
    for y in range(0,6,3):
        if state[y] == state[y+1] == state[y+2]:
            return True
    if state[0] == state[4] == state[8]:
        return True
    if state[2] == state[4] == state[6]:
        return True
    for (y) in range(len(state)):
        if type(state[y]) is int:
            return False
    return True

def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    x,o = "X","O"
    if is_terminal(state):
        for (y) in range(3):
            if state[y] == state[y + 3] == state[y + 6]:
                if state[y]== x:
                    return 1
                return -1
        for y in range(0, 6, 3):
            if state[y] == state[y + 1] == state[y + 2]:
                if state[y] == x:
                    return 1
                return -1
        if state[0] == state[4] == state[8]:
            if state[0]== x:
                return 1
            return -1
        if state[2] == state[4] == state[6]:
            if state[2]== x:
                return 1
            return -1
        return 0



def successors_of(state):
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    x,o = "X","O"
    states = []
    stateCount = state.count(x) <= state.count(o)
    for y in range(len(state)):
      if type(state[y]) is int:
        copyState = state.copy()
        copyState[y] = x if stateCount else o
        states.append((y,copyState))
    return states


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
