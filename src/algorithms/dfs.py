def get_children(position, maze, visited):
    x, y = position
    v = maze[x][y]
    childs = []
    max_row = len(maze)
    max_col = len(maze[0])

    directions = [
        (x - v, y),
        (x + v, y),
        (x, y - v),
        (x, y + v)
    ]

    for new_x, new_y in directions:
        if 0 <= new_x < max_row and 0 <= new_y < max_col:
            if (new_x, new_y) not in visited:
                childs.append((new_x, new_y))

    return childs

def dfs_recursive(full_path, valid_path, actual, end, maze):
    full_path.append(actual)

    if actual == end:
        valid_path.append(actual)
        return True

    children = get_children(actual, maze, full_path)

    for child in children:
        if dfs_recursive(full_path, valid_path, child, end, maze):
            valid_path.append(actual)
            return True

    return False

def dfs(data, maze):
    data = list(map(int, data.split()))
    maze = [list(map(int, row.split())) for row in maze]

    full_path = []
    valid_path = []

    start = (data[2], data[3])
    end = (data[4], data[5])

    found = dfs_recursive(full_path, valid_path, start, end, maze)

    if found:
        valid_path = valid_path[::-1]


    return [maze, full_path, valid_path]
