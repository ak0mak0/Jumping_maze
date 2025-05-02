def get_children(position, maze, visited):
    x, y = position
    v = maze[x][y]
    children = []
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
                children.append((new_x, new_y))
    return children

def ucs_v1(data, maze):
    data = list(map(int, data.split()))
    maze = [list(map(int, fila.split())) for fila in maze]

    full_path = []
    valid_path = []

    start = (data[2], data[3])
    end = (data[4], data[5])

    heap = [(0, start)]
    accumulated = {start: 0}
    record = {}

    while heap:
        heap.sort()
        current_cost, current = heap.pop(0)
        full_path.append(current)

        if current == end:
            break

        for child in get_children(current, maze, full_path):
            new_cost = current_cost + maze[child[0]][child[1]]
            if child not in accumulated or new_cost < accumulated[child]:
                accumulated[child] = new_cost
                heap.append((new_cost, child))
                record[child] = current


    if end in record or start == end:
        current = end
        while current != start:
            valid_path.append(current)
            current = record[current]
        valid_path.append(start)
        valid_path.reverse()

    return [maze, full_path, valid_path]
