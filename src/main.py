import pygame
from pygame._sdl2 import Window

from interpreter import read_mazes
from algorithms.dfs import dfs
from algorithms.ucs_v1 import ucs_v1
from algorithms.ucs_v2 import ucs_v2

from engine import Engine
from screens.interface_screen import InterfaceScreen

def main():
    filename = "input/test.txt"
    datas, mazes = read_mazes(filename)

    mtx_results = []
    path_results = []

    if datas and mazes:
        for i in range(len(datas)):
            maze_data = datas[i]
            maze_text = mazes[i]

            dfs_result = dfs(maze_data, maze_text)
            ucs_v1_result = ucs_v1(maze_data, maze_text)
            ucs_v2_result = ucs_v2(maze_data, maze_text)

            mtx_results.append(dfs_result[0])
            path_results.append([dfs_result[1:], ucs_v1_result[1:], ucs_v2_result[1:]])
    else:
        print("No se pudieron procesar los laberintos.")
        return

    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)
    Window.from_display_module().maximize()
    pygame.display.set_caption("Jumping Maze")

    engine = Engine(window)
    interface_screen = InterfaceScreen(engine, mtx_results, path_results)

    engine.set_screen(interface_screen)
    engine.run(window, clock)

    pygame.quit()

if __name__ == "__main__":
    main()