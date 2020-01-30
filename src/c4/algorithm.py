
from utils.constants import C4_ROW_NUMBER, C4_COLUMN_NUMBER
def check_map(map):
    win = []
    for col in range(C4_COLUMN_NUMBER):
        row = get_last_row(map, col)
        if row != -1:
            result = check_position(map, row, col)
            if result:
                win.extend(result)
    if win:
        return (True, get_win_map(map, win))
    return (False, map)

def get_win_map(map, win):
    for win_case in win:
        change_map(map, win_case)
    return map

def change_map(map, win_case):
    row, col, method = win_case
    map[row][col] = 3
    if method == 'h':
        for i in range(1, 4): map[row][col+i] = 3
    elif method == 'v':
        for i in range(1, 4): map[row+i][col] = 3
    elif method == 'dl':
        for i in range(1, 4): map[row+i][col-i] = 3
    elif method == 'dr':
        for i in range(1, 4): map[row+i][col+i] = 3

def check_position(map, row, col):
    win = []
    user_value = map[row][col]
    print(f'{row=}, {col=}, {user_value=}')
    # Horizontal check
    if col + 3 < C4_COLUMN_NUMBER:
        if all([1 if map[row][col+i] == user_value else 0 for i in range(1, 4)]):
            print('Horizontal')
            win.append((row, col, 'h'))

    # Vertical check
    if row + 3 < C4_ROW_NUMBER:
        if all([1 if map[row+i][col] == user_value else 0 for i in range(1, 4)]):
            print('Vertical')
            win.append((row, col, 'v'))

    # Diagonal /
    if col - 3 >= 0 and row + 3 < C4_ROW_NUMBER:
        if all([1 if map[row+i][col-i] == user_value else 0 for i in range(1, 4)]):
            print("Diagonal /")
            win.append((row, col, 'dl'))

    # Diagonal \
    if col + 3 < C4_COLUMN_NUMBER and row + 3 < C4_ROW_NUMBER:
        if all([1 if map[row+i][col+i] == user_value else 0 for i in range(1, 4)]):
            print("Diagonal \\")
            win.append((row, col, 'dr'))

    return win

def get_last_row(map, col):
    for i in range(C4_ROW_NUMBER):
        if map[i][col]:
            return i
    return -1 