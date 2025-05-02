from typing import Self, Optional
import pygame
from pygame.font import Font
from components.element import Element
from events import Event


class Text(Element):
    _text: str
    _font: Font
    _color: tuple[int, int, int]
    _lines: list[str]
    _line_surfaces: list[pygame.Surface]
    _max_chars_per_line: Optional[int]

    def __init__(self, text: str, font: Font, color: tuple[int, int, int], max_chars_per_line: Optional[int] = None):
        self._text = text
        self._font = font
        self._color = color
        self._max_chars_per_line = max_chars_per_line

        self._lines = self._wrap_text(text)
        self._line_surfaces = [font.render(line, True, color) for line in self._lines]

        width = max(surface.get_width() for surface in self._line_surfaces)
        height = sum(surface.get_height() for surface in self._line_surfaces)

        super().__init__(width, height)

    def _wrap_text(self, text: str) -> list[str]:
        if not self._max_chars_per_line:
            return [text]
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            if len(current_line + ' ' + word) <= self._max_chars_per_line:
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def set_position(self, position: tuple[int, int]) -> Self:
        self._position = position
        return self

    def set_text(self, text: str) -> Self:
        self._text = text
        self._lines = self._wrap_text(text)
        self._line_surfaces = [self._font.render(line, True, self._color) for line in self._lines]
        self._width = max(surface.get_width() for surface in self._line_surfaces)
        self._height = sum(surface.get_height() for surface in self._line_surfaces)
        return self

    def set_color(self, color: tuple[int, int, int]) -> Self:
        self._color = color
        self._line_surfaces = [self._font.render(line, True, color) for line in self._lines]
        return self

    def set_font(self, font: Font) -> Self:
        self._font = font
        self._line_surfaces = [font.render(line, True, self._color) for line in self._lines]
        self._width = max(surface.get_width() for surface in self._line_surfaces)
        self._height = sum(surface.get_height() for surface in self._line_surfaces)
        return self

    def on_any_event(self, event: Event) -> None:
        pass

    def render(self, window) -> None:
        x, y = self._position
        for surface in self._line_surfaces:
            window.blit(surface, (x, y))
            y += surface.get_height()

    def set_max_chars_per_line(self, max_chars: int) -> Self:
        self._max_chars_per_line = max_chars
        self._lines = self._wrap_text(self._text)
        self._line_surfaces = [self._font.render(line, True, self._color) for line in self._lines]
        self._width = max(surface.get_width() for surface in self._line_surfaces)
        self._height = sum(surface.get_height() for surface in self._line_surfaces)
        return self

    def set_font_size(self, size: int) -> Self:
        self._font = pygame.font.Font(None, size)
        self._line_surfaces = [self._font.render(line, True, self._color) for line in self._lines]
        self._width = max(surface.get_width() for surface in self._line_surfaces)
        self._height = sum(surface.get_height() for surface in self._line_surfaces)
        return self