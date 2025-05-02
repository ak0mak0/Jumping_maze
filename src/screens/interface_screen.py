import pygame

from assets import FontManager
from components import ChildAlignment, Column, Container, HorizontalAlignment, Row, Text, Board
from engine import Engine
from events import Event, EventType, KeyEvent, MouseButton, MouseButtonEvent, MouseMotionEvent, QuitEvent
from screens.screen import Screen


class InterfaceScreen(Screen):
    _engine: Engine

    def __init__(self, engine: Engine, mtx_results: list, path_results: list):
        self._paths = path_results
        self._engine = engine
        self._width, self._height = engine.window_size

        self._base = Container(self._width, self._height)
        self._base.set_child_alignment(ChildAlignment.CENTER)

        self._column1 = Column().set_padding(20)
        self._row1 = Row().set_padding(0)

        # ----- DISPOCISION TABLERO -----
        _controls = Container(int(self._width * 0.4), int(self._height)).set_background_color((198, 206, 205, 100)).set_child_alignment(ChildAlignment.TOP_CENTER)
        _board = Container(int(self._width * 0.6), int(self._height)).set_background_color((198, 206, 205, 0)).set_child_alignment(ChildAlignment.CENTER)
        _board.set_child(self._column1)

        self._row1.add_element(_controls)
        self._row1.add_element(_board)

        self._board_container = Container(int(self._height * 0.7), int(self._height * 0.7))
        self._board_container.set_background_color((198, 206, 205, 0))
        self._board_container.set_child_alignment(ChildAlignment.CENTER)

        # ----- BOTONES -----
        self._row_button1 = Row().set_padding(10)
        self._button1 = Container(int(self._height * 0.07), int(self._height * 0.07))
        self._button1.set_background_color((166, 166, 198, 250))
        self._button2 = Container(int(self._height * 0.2), int(self._height * 0.07))
        self._button2.set_background_color((166, 166, 198, 250))
        self._button3 = Container(int(self._height * 0.07), int(self._height * 0.07))
        self._button3.set_background_color((166, 166, 198, 250))
        self._button1.set_child(Text("<", engine.regular_font, (0, 0, 0)))
        self._button2.set_child(Text("matriz", engine.regular_font, (0, 0, 0)))
        self._button3.set_child(Text(">", engine.regular_font, (0, 0, 0)))
        self._row_button1.add_element(self._button1)
        self._row_button1.add_element(self._button2)
        self._row_button1.add_element(self._button3)
        self._column1.add_element(self._row_button1)

        self._row_button2 = Row().set_padding(10)
        self._button4 = Container(int(self._height * 0.07), int(self._height * 0.07))
        self._button4.set_background_color((176, 232, 226, 255))
        self._button5 = Container(int(self._height * 0.2), int(self._height * 0.07))
        self._button5.set_background_color((176, 232, 226, 255))
        self._button6 = Container(int(self._height * 0.07), int(self._height * 0.07))
        self._button6.set_background_color((176, 232, 226, 255))
        self._button4.set_child(Text("<", engine.regular_font, (0, 0, 0)))
        self._button5.set_child(Text("algoritmo", engine.regular_font, (0, 0, 0)))
        self._button6.set_child(Text(">", engine.regular_font, (0, 0, 0)))
        self._row_button2.add_element(self._button4)
        self._row_button2.add_element(self._button5)
        self._row_button2.add_element(self._button6)

        # ----- ZONA BOTONES -----

        title = Container(int(self._width * 0.25), int(self._height * 0.15)).set_background_color(
            (144, 168, 241, 220)).set_child_alignment(ChildAlignment.CENTER).set_child(Text("<<< jumping maze >>>", engine.regular_font, (0, 0, 0)))
        algorithm_name_zone = Container(int(self._width * 0.4), int(self._height * 0.15)).set_background_color(
            (144, 168, 241, 0)).set_child_alignment(ChildAlignment.CENTER_RIGHT)
        color_name_zone = Container(int(self._width * 0.25), int(self._height * 0.15)).set_background_color(
            (241, 156, 144, 255)).set_child_alignment(ChildAlignment.CENTER)
        column_dynamic_name = Column().set_padding(10)

        self._dynamic_name = Container(int(self._width * 0.4), int(self._height * 0.06)).set_child(Text("Depth-first search", engine.regular_font, (0, 0, 0)))

        column_dynamic_name.add_element(self._dynamic_name)
        column_dynamic_name.add_element(self._row_button2)

        color_name_zone.set_child(column_dynamic_name)
        algorithm_name_zone.set_child(color_name_zone)


        controls_row = Row()
        self._back = Container(int(self._width * 0.05), int(self._height * 0.15)).set_background_color(
            (229, 145, 176, 255)).set_child_alignment(ChildAlignment.CENTER).set_child(Text("", engine.regular_font, (0, 0, 0)))
        controls_column = Column()
        self._apply_algorithm = Container(int(self._width * 0.2), int(self._height * 0.15/2)).set_background_color(
            (255, 189, 93, 255)).set_child_alignment(ChildAlignment.CENTER).set_child(
            Text("apply algorithm", engine.regular_font, (0, 0, 0)))
        self._resolve = Container(int(self._width * 0.2), int(self._height * 0.15/2)).set_background_color(
            (175, 243, 141, 149)).set_child_alignment(ChildAlignment.CENTER).set_child(
            Text("solve jumping maze", engine.regular_font, (0, 0, 0)))
        controls_column.add_element(self._apply_algorithm)
        controls_column.add_element(self._resolve)
        self._next = Container(int(self._width * 0.05), int(self._height * 0.15)).set_background_color(
            (229, 145, 176, 255)).set_child_alignment(ChildAlignment.CENTER).set_child(Text("", engine.regular_font, (0, 0, 0)))

        controls_row.add_element(self._back)
        controls_row.add_element(controls_column)
        controls_row.add_element(self._next)

        info = Container(int(self._width * 0.4), int(self._height * 0.4)+95).set_background_color(
            (144, 168, 241, 0)).set_child_alignment(ChildAlignment.BOTTOM_RIGHT)
        progress = Container(int(self._width * 0.4), int(self._height * 0.45)).set_background_color(
            (144, 168, 241, 150)).set_child_alignment(ChildAlignment.TOP_CENTER)
        progress_title = Text("Progress", engine.regular_font, (0, 0, 0))
        progress_column = Column()
        full_path = Container(int(self._width * 0.4), int(((self._height * 0.38 - progress_title._height) / 2) +self._height * 0.07)).set_background_color(
            (0, 255, 255, 255)).set_child_alignment(ChildAlignment.TOP_LEFT)
        solved_path = Container(int(self._width * 0.4), int((self._height * 0.38 - progress_title._height) / 2)).set_background_color(
            (255, 0, 255, 255)).set_child_alignment(ChildAlignment.TOP_LEFT)
        self._dynamic_full_path = Text("...", engine.regular_font, (0, 0, 0)).set_max_chars_per_line(137).set_font_size(20)
        full_path.set_child(
            Column()
            .add_element(Text("Full path", engine.regular_font, (0, 0, 0)))
            .add_element(self._dynamic_full_path)
        )
        self._dynamic_solved_path = Text("...", engine.regular_font, (0, 0, 0)).set_max_chars_per_line(137).set_font_size(20)
        solved_path.set_child(
            Column()
            .add_element(Text("Solved path", engine.regular_font, (0, 0, 0)))
            .add_element(self._dynamic_solved_path)
        )
        progress_column.add_element(progress_title)
        progress_column.add_element(full_path)
        progress_column.add_element(solved_path)

        progress.set_child(progress_column)
        info.set_child(progress)



        button_column = Column().set_padding(20)
        button_column.add_element(title)
        button_column.add_element(algorithm_name_zone)
        button_column.add_element(controls_row)
        button_column.add_element(info)
        _controls.set_child(button_column)

        # ----- IMPLEMENTACION TABLERO -----
        self._actual_board = 0
        self._actual_algorithm = 0

        self._mazes_data = mtx_results
        self._full_path_selected = self._paths[self._actual_board][self._actual_algorithm][0]
        self._valid_path = self._paths[self._actual_board][self._actual_algorithm][1]
        self._maze_selected = self._mazes_data[self._actual_board]

        padding = 2
        self._board = Board(
            block_size=int(min(
                self._board_container._width / len(self._maze_selected),
                self._board_container._width / len(self._maze_selected[0])
            )),
            padding=padding,
            matrix=self._maze_selected,
            engine=engine
        )
        self._board.set_path(self._full_path_selected)
        self._board_container.set_child(self._board)
        self._column1.add_element(self._board_container)


        self._base.set_child(self._row1)

    def on_any_event(self, event: Event) -> None:
        pass

    def on_key_event(self, key_event: KeyEvent) -> None:
        pass

    def on_mouse_button_event(self, event: MouseButtonEvent) -> None:

        if event.type != EventType.MOUSE_BUTTON_DOWN or event.button != MouseButton.LEFT:
            return

        mouse_pos = pygame.mouse.get_pos()

        if self._button1.contains(mouse_pos):
            if self._actual_board != 0:
                self._actual_board = self._actual_board - 1
                self._maze_selected = self._mazes_data[self._actual_board]
                self._full_path_selected = self._paths[self._actual_board][self._actual_algorithm][0]
                self._valid_path = self._paths[self._actual_board][self._actual_algorithm][1]
                self._board.set_matrix(self._maze_selected)
                self._board.set_path(self._full_path_selected)
                self._board.set_block_size(int(min(
                    self._board_container._width / len(self._maze_selected),
                    self._board_container._width / len(self._maze_selected[0])
                )))
                self._dynamic_full_path.set_text("...")
                self._dynamic_solved_path.set_text("...")
                self._board.stop_animation()

        if self._button4.contains(mouse_pos):
            if self._actual_algorithm != 0:
                self._actual_algorithm = self._actual_algorithm - 1
                self._maze_selected = self._mazes_data[self._actual_algorithm]
                self._full_path_selected = self._paths[self._actual_board][self._actual_algorithm][0]
                self._valid_path = self._paths[self._actual_board][self._actual_algorithm][1]
                self._board.set_path(self._full_path_selected)
                if self._actual_algorithm == 0:
                    self._dynamic_name.set_child(Text("Depth-first search", self._engine.regular_font, (0, 0, 0)))
                if self._actual_algorithm == 1:
                    self._dynamic_name.set_child(Text("Uniform-Cost Search v1", self._engine.regular_font, (0, 0, 0)))
                if self._actual_algorithm == 2:
                    self._dynamic_name.set_child(Text("Uniform-Cost Search v2", self._engine.regular_font, (0, 0, 0)))
                self._dynamic_full_path.set_text("...")
                self._dynamic_solved_path.set_text("...")
                self._board.stop_animation()

        if self._apply_algorithm.contains(mouse_pos):
            self._board.set_path(self._full_path_selected)
            self._board.start_animation()
            self._dynamic_full_path.set_text(str(self._full_path_selected))


        if self._resolve.contains(mouse_pos):
            self._board.set_path(self._valid_path)
            self._board.start_animation()
            self._dynamic_solved_path.set_text(str(self._valid_path))

        if self._button3.contains(mouse_pos):
            if self._actual_board != len(self._mazes_data) - 1:
                self._actual_board = self._actual_board + 1
                self._maze_selected = self._mazes_data[self._actual_board]
                self._full_path_selected = self._paths[self._actual_board][self._actual_algorithm][0]
                self._valid_path = self._paths[self._actual_board][self._actual_algorithm][1]
                self._board.set_matrix(self._maze_selected)
                self._board.set_path(self._full_path_selected)
                self._board.set_block_size(int(min(
                    self._board_container._width / len(self._maze_selected),
                    self._board_container._width / len(self._maze_selected[0])
                )))
                self._dynamic_full_path.set_text("...")
                self._dynamic_solved_path.set_text("...")
                self._board.stop_animation()

        if self._button6.contains(mouse_pos):
            if self._actual_algorithm != len(self._paths[0]) - 1:
                self._actual_algorithm = self._actual_algorithm + 1
                self._maze_selected = self._mazes_data[self._actual_algorithm]
                self._full_path_selected = self._paths[self._actual_board][self._actual_algorithm][0]
                self._valid_path = self._paths[self._actual_board][self._actual_algorithm][1]
                self._board.set_path(self._full_path_selected)
                if self._actual_algorithm==0:
                    self._dynamic_name.set_child(Text("Depth-first search", self._engine.regular_font, (0, 0, 0)))
                if self._actual_algorithm==1:
                    self._dynamic_name.set_child(Text("Uniform-Cost Search v1", self._engine.regular_font, (0, 0, 0)))
                if self._actual_algorithm==2:
                    self._dynamic_name.set_child(Text("Uniform-Cost Search v2", self._engine.regular_font, (0, 0, 0)))
                self._dynamic_full_path.set_text("...")
                self._dynamic_solved_path.set_text("...")
                self._board.stop_animation()

    def on_mouse_motion_event(self, event: MouseMotionEvent) -> None:
        pass

    def on_quit_event(self, key_event: QuitEvent) -> None:
        pass

    def render(self) -> None:
        window = pygame.display.get_surface()
        self._board.update()
        self._base.render(window)
        self._board.render(window)