
from utils.constants import C4_ROW_NUMBER, C4_COLUMN_NUMBER


def check_map(game_map):
    """Check whether game_map has a winner. If so -> change game_map

    Arguments:
        game_map {matrix (list of lists)} -- game map matrix

    Returns:
        Tuple(bool, matrix) --
            bool - if game_map has a winner
            matrix - game_map
    """
    win = []
    for col in range(C4_COLUMN_NUMBER):
        if game_map[-1][col]:  # if col of game map isn't empty
            row = get_last_row(game_map, col)
            result = check_position(game_map, row, col)
            if result:
                win.extend(result)
    if win:
        return (True, get_win_map(game_map, win))
    return (False, game_map)

def get_win_map(game_map, win):
    """Having win combinations change game_map to win_game_map

    Arguments:
        game_map {matrix} -- game map
        win {list} -- win combinations

    Returns:
        matrix -- changed game map
    """
    for win_case in win:
        change_map(game_map, win_case)
    return game_map

def change_map(game_map, win_case):
    #TODO - enum for win methods
    """Having 1 particular win case - change game map

    Arguments:
        game_map {matrix} -- game map
        win_case {tuple(row, col, method)} --
            - row - y of step of which win case starts
            - col - x of step of which win case starts
            - method - win case method
    """
    row, col, method = win_case
    game_map[row][col] = 3
    if method == 'h':
        for i in range(1, 4):
            game_map[row][col+i] = 3
    elif method == 'v':
        for i in range(1, 4):
            game_map[row+i][col] = 3
    elif method == 'dl':
        for i in range(1, 4):
            game_map[row+i][col-i] = 3
    elif method == 'dr':
        for i in range(1, 4):
            game_map[row+i][col+i] = 3

def check_position(game_map, row, col):
    #TODO - enum for win methods
    """Check if step on (row, col) (y, x) has a win combination

    Arguments:
        game_map {matrix} -- game map
        row {int} -- position's row (y)
        col {int} -- position's column (x)

    Returns:
        list -- step's on (row, col) (y, x) win combinations
    """
    win = []
    user_value = game_map[row][col]
    # print(f'{row=}, {col=}, {user_value=}')
    # Horizontal check
    if col + 3 < C4_COLUMN_NUMBER:
        if all([1 if game_map[row][col+i] == user_value else 0 for i in range(1, 4)]):
            win.append((row, col, 'h'))

    # Vertical check
    if row + 3 < C4_ROW_NUMBER:
        if all([1 if game_map[row+i][col] == user_value else 0 for i in range(1, 4)]):
            win.append((row, col, 'v'))

    # Diagonal /
    if col - 3 >= 0 and row + 3 < C4_ROW_NUMBER:
        if all([1 if game_map[row+i][col-i] == user_value else 0 for i in range(1, 4)]):
            win.append((row, col, 'dl'))

    # Diagonal \
    if col + 3 < C4_COLUMN_NUMBER and row + 3 < C4_ROW_NUMBER:
        if all([1 if game_map[row+i][col+i] == user_value else 0 for i in range(1, 4)]):
            win.append((row, col, 'dr'))

    return win

def get_last_row(game_map, col):
    """Return row of first existing step from top on given col

    Arguments:
        game_map {matrix} -- game map
        col {int} -- game map's column

    Returns:
        int -- row of step from top
    """
    for i in range(C4_ROW_NUMBER):
        if game_map[i][col]:
            return i
    return -1
