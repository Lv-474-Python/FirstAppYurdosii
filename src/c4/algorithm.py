from utils.constants import C4_ROW_NUMBER, C4_COLUMN_NUMBER
from utils.enums import MapValue, WinMethod


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
            if row != -1:
                win.extend(check_position(game_map, row, col))
    if win:
        win = list(set(win))
        return (True, get_win_map(game_map, win))
    return (False, game_map)

def get_win_map(game_map, win):
    """Having win combinations change game_map

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
    """Having 1 particular win case - change game map

    Arguments:
        game_map {matrix} -- game map
        win_case {tuple(int, int, WinMethod)} --
            - int - y (row) of step of which win case starts
            - int - x (col) of step of which win case starts
            - WinMethod - win case method
    """
    row, col, method = win_case
    if method is WinMethod.HORIZONTAL:
        for i in range(4):
            game_map[row][col+i] = MapValue.WINNER
    elif method is WinMethod.VERTICAL:
        for i in range(4):
            game_map[row+i][col] = MapValue.WINNER
    elif method is WinMethod.DIAGONAL_LEFT:
        for i in range(4):
            game_map[row+i][col-i] = MapValue.WINNER
    elif method is WinMethod.DIAGONAL_RIGHT:
        for i in range(4):
            game_map[row+i][col+i] = MapValue.WINNER

def check_position(game_map, row, col):
    """Check if step on (row, col) (y, x) inside win combinations

    Arguments:
        game_map {matrix} -- game map
        row {int} -- position's row (y)
        col {int} -- position's column (x)

    Returns:
        list -- win combinations
    """
    win = []
    user_value = game_map[row][col]

    # Horizontal check
    result = check_position_horizontal(game_map, row, col, user_value)
    win.extend(result)

    # Vertical check
    result = check_position_vertical(game_map, row, col, user_value)
    win.extend(result)

    # Diagonal /
    result = check_position_diagonal_left(game_map, row, col, user_value)
    win.extend(result)

    # Diagonal \
    result = check_position_diagonal_right(game_map, row, col, user_value)
    win.extend(result)

    return win

def check_position_horizontal(game_map, row, col, user_value):
    """Check for horizontal win cases

    Arguments:
        game_map {matrix} -- game map
        row {int} -- position's row (y)
        col {int} -- position's column (x)
        user_value {MapValue} -- user value at (x, y)

    Returns:
        list -- horizontal win cases
    """
    _, _, left, right = get_position_limits(row, col)
    right += 1

    win_cases = []
    for i in range(left, right - 4 + 1):
        if all([1 if game_map[row][j] == user_value else 0 for j in range(i, i + 4)]):
            win_cases.append((row, i, WinMethod.HORIZONTAL))
    return win_cases

def check_position_vertical(game_map, row, col, user_value):
    """Check for vertical win cases

    Arguments:
        game_map {matrix} -- game map
        row {int} -- position's row (y)
        col {int} -- position's column (x)
        user_value {MapValue} -- user value at (x, y)

    Returns:
        list -- vertical win cases
    """
    high, low, _, _ = get_position_limits(row, col)
    low += 1

    win_cases = []
    for i in range(high, low - 4 + 1):
        if all([1 if game_map[j][col] == user_value else 0 for j in range(i, i + 4)]):
            win_cases.append((i, col, WinMethod.VERTICAL))
    return win_cases

def check_position_diagonal_left(game_map, row, col, user_value):
    """Check for diagonal left (/) win cases

    Arguments:
        game_map {matrix} -- game map
        row {int} -- position's row (y)
        col {int} -- position's column (x)
        user_value {MapValue} -- user value at (x, y)

    Returns:
        list -- diagonal left win cases
    """
    high, low, left, right = get_position_limits(row, col)

    # change right and high
    less_diff = right - col if right - col < row - high else row - high
    right = col + less_diff
    high = row - less_diff

    # change left and low
    less_diff = col - left if col - left < low - row else low - row
    left = col - less_diff
    low = row + less_diff

    # calculate win cases
    win_cases = []
    number_of_fours = get_number_of_fours(high, low, left, right)
    for i in range(number_of_fours):
        if all([1 if game_map[high+i+j][right-i-j] == user_value else 0 for j in range(0, 4)]):
            win_cases.append((high+i, right-i, WinMethod.DIAGONAL_LEFT))
    return win_cases

def check_position_diagonal_right(game_map, row, col, user_value):
    """Check for diagonal right (\\) win cases

    Arguments:
        game_map {matrix} -- game map
        row {int} -- position's row (y)
        col {int} -- position's column (x)
        user_value {MapValue} -- user value at (x, y)

    Returns:
        list -- diagonal right win cases
    """
    high, low, left, right = get_position_limits(row, col)

    # change left and high
    less_diff = col - left if col - left < row - high else row - high
    left = col - less_diff
    high = row - less_diff

    # change right and low
    less_diff = right - col if right - col < low - row else low - row
    right = col + less_diff
    low = row + less_diff

    # calculate win cases
    win_cases = []
    number_of_fours = get_number_of_fours(high, low, left, right)
    for i in range(number_of_fours):
        if all([1 if game_map[high+i+j][left+i+j] == user_value else 0 for j in range(0, 4)]):
            win_cases.append((high+i, left+i, WinMethod.DIAGONAL_RIGHT))
    return win_cases

def get_position_limits(row, col):
    """Given position's row(y) and col(x) return it's high, low, left, right limits

    Arguments:
        row {int} -- position's row (y)
        col {int} -- position's column (x)

    Returns:
        tuple(int, int, int, int) -- tuple with high, low, left and right position limits
    """
    high = 0 if row - 3 <= 0 else row - 3
    low = C4_ROW_NUMBER - 1 if row + 3 >= C4_ROW_NUMBER else row + 3
    left = 0 if col - 3 <= 0 else col - 3
    right = C4_COLUMN_NUMBER - 1 if col + 3 >= C4_COLUMN_NUMBER else col + 3
    return (high, low, left, right)

def get_number_of_fours(high, low, left, right):
    """Return number of fours that possible in diagonal by given limits

    Arguments:
        high {int} -- position's high limit
        low {int} -- position's low limit
        left {int} -- position's low limit
        right {[type]} -- position's right limit

    Returns:
        int -- number of fours
    """
    number_of_fours = int(((left-right)**2 + (low-high)**2)**0.5) - 4 + 1
    number_of_fours = 3 if number_of_fours >= 3 else number_of_fours
    return number_of_fours

def get_last_row(game_map, col):
    """Return row of first existing step from top on given col

    Arguments:
        game_map {matrix} -- game map
        col {int} -- game map's column

    Returns:
        int -- row of step from top
    """
    for i in range(C4_ROW_NUMBER):
        if game_map[i][col] in [MapValue.PLAYER_1, MapValue.PLAYER_2]:
            return i
    return -1
