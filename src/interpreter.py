def lineverificator(line, expected_parts=None):
    parts = line.split()
    if expected_parts and len(parts) != expected_parts:
        return False
    return all(part.isdigit() for part in parts)

def read_mazes(filename):
    mazes = []
    datas = []

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        line_index = 0

        while line_index < len(lines):
            line = lines[line_index].strip()

            if not line:
                line_index += 1
                continue

            maze = []

            if lineverificator(line, 6):
                datas.append(line)
                m, n, initial_x, initial_y, final_x, final_y = map(int, line.split())

                if not (0 <= initial_x < m and 0 <= initial_y < n):
                    raise ValueError("Posición inicial fuera de los límites.")
                if not (0 <= final_x < m and 0 <= final_y < n):
                    raise ValueError("Posición final fuera de los límites.")

                line_index += 1
                for _ in range(m):
                    if line_index >= len(lines):
                        raise ValueError("Fila fuera de rango")

                    row = lines[line_index].strip()
                    if lineverificator(row) and len(row.split()) == n:
                        maze.append(row)
                    else:
                        raise ValueError("Fila incorrecta")
                    line_index += 1

            else:
                raise ValueError("Línea de configuración incorrecta")

            mazes.append(maze)

    except FileNotFoundError:
        print("Archivo no encontrado:", filename)
        return [], []

    except ValueError as ve:
        print("--- ERROR ---")
        print(str(ve))
        return [], []

    return datas, mazes
