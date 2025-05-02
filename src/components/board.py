from typing import Self
import pygame
import time

from select import select

from components.element import Element
from events import Event, EventType, MouseButton


class Board(Element):
    def __init__(self, block_size: int, padding: int, matrix: list[list[int]], engine=None) -> None:
        self._block_size = block_size
        self._padding = padding
        self._matrix = matrix
        self._rows = len(matrix)
        self._cols = len(matrix[0]) if matrix else 0
        self._selected_position = None  # (row, col)
        self._path = []
        self._path_index = 0
        self._animating = False
        self._animation_speed = 100*len(matrix)
        self._last_update = 0
        self._engine = engine

        width = self._cols * (block_size + padding) - padding
        height = self._rows * (block_size + padding) - padding
        super().__init__(width, height)

        self._font = pygame.font.SysFont(None, int(block_size * 0.6))
        self._surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self._surface.fill((255, 255, 255, 128))

    def set_position(self, position: tuple[int, int]) -> Self:
        self._position = position
        return self

    def on_any_event(self, event: Event) -> None:
        if event.type != EventType.MOUSE_BUTTON_DOWN or event.button != MouseButton.LEFT:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        x0, y0 = self._position

        for row in range(self._rows):
            for col in range(self._cols):
                x = x0 + col * (self._block_size + self._padding)
                y = y0 + row * (self._block_size + self._padding)
                rect = pygame.Rect(x, y, self._block_size, self._block_size)

                if rect.collidepoint(mouse_x, mouse_y):
                    self._selected_position = (row, col)
                    return

    def get_selected_position(self) -> tuple[int, int] | None:
        return self._selected_position

    def set_path(self, path: list[tuple[int, int]]) -> None:
        self._path = path
        self._path_index = 0
        self._animation_speed = 25*len(path)
        if path:
            self._selected_position = path[0]

    def set_matrix(self, matrix: list[list[int]]) -> None:
        self._matrix = matrix
        self._rows = len(matrix)
        self._cols = len(matrix[0]) if matrix else 0
        self._animation_speed = 100 * len(matrix)

    def set_block_size(self, block_size: int) -> None:
        self._block_size = block_size
        self._font = pygame.font.SysFont(None, block_size // 2)

    def animate(self) -> None:
        self._animating = True
        self._path_index = 0
        self._last_update = pygame.time.get_ticks()

    def update(self) -> None:
        if self._animating and self._path_index < len(self._path):
            now = pygame.time.get_ticks()
            if now - self._last_update >= self._animation_speed:
                self._selected_position = self._path[self._path_index]
                self._path_index += 1
                self._last_update = now
        elif self._path_index >= len(self._path):
            self._animating = False

    def render(self, screen) -> None:
        x0, y0 = self._position

        for row in range(self._rows):
            for col in range(self._cols):
                x = x0 + col * (self._block_size + self._padding)
                y = y0 + row * (self._block_size + self._padding)
                rect = pygame.Rect(x, y, self._block_size, self._block_size)

                if (row, col) == self._selected_position:
                    color = (255, 100, 100)
                elif self._path and (row, col) == self._path[0]:
                    color = (180, 180, 180)  # Gris
                elif self._path and (row, col) == self._path[-1]:
                    color = (0, 200, 0)  # Verde
                else:
                    color = (255, 255, 255)

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

                value = self._matrix[row][col]
                font = pygame.font.SysFont(None, int(self._block_size * 0.6))
                text_surface = font.render(str(value), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    def start_animation(self) -> None:
        self._animating = True
        self._path_index = 1
        self._last_update = pygame.time.get_ticks()

    def stop_animation(self) -> None:
        self._animating = False
        self._path_index = 0
        self._selected_position = self._path[0] if self._path else None