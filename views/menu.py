import arcade
import arcade.gui

from .game import GameView


class MenuView(arcade.View):
    def __init__(self, main_view):
        super().__init__()

        self.main_view = main_view
        self.manager = arcade.gui.UIManager()

        self.show_controls = False
        self.time = 0

        self.setup_ui()

    def setup_ui(self):
        title = arcade.gui.UILabel(
            text="SURVIVAL ISLAND",
            font_size=42,
            text_color=arcade.color.WHITE,
            align="center",
        )

        subtitle = arcade.gui.UILabel(
            text="Find food, complete quests and escape the island",
            font_size=15,
            text_color=arcade.color.LIGHT_GRAY,
            align="center",
        )

        play_button = arcade.gui.UIFlatButton(
            text="Play",
            width=230,
            height=45,
        )
        play_button.on_click = self.on_play_click

        controls_button = arcade.gui.UIFlatButton(
            text="Controls",
            width=230,
            height=45,
        )
        controls_button.on_click = self.on_controls_click

        quit_button = arcade.gui.UIFlatButton(
            text="Quit",
            width=230,
            height=45,
        )
        quit_button.on_click = self.on_quit_click

        menu_box = arcade.gui.UIBoxLayout(
            vertical=True,
            space_between=18,
        )

        menu_box.add(title)
        menu_box.add(subtitle)
        menu_box.add(play_button)
        menu_box.add(controls_button)
        menu_box.add(quit_button)

        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(
            child=menu_box,
            anchor_x="center_x",
            anchor_y="center_y",
        )

    def on_play_click(self, event):
        game = GameView()
        game.setup()
        self.main_view.show_view(game)

    def on_controls_click(self, event):
        self.show_controls = not self.show_controls

    def on_quit_click(self, event):
        arcade.exit()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_update(self, delta_time):
        self.time += delta_time

    def on_draw(self):
        self.clear()

        self.draw_background()
        self.manager.draw()

        if self.show_controls:
            self.draw_controls_panel()

        self.draw_footer()

    def draw_background(self):
        width = self.window.width
        height = self.window.height

        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                width / 2,
                height / 2,
                width,
                height,
            ),
            arcade.color.DARK_BLUE,
        )

        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                width / 2,
                130,
                width,
                260,
            ),
            arcade.color.BLUE_GREEN,
        )

        arcade.draw_ellipse_filled(
            width / 2,
            150,
            520,
            170,
            arcade.color.SAND,
        )

        arcade.draw_ellipse_filled(
            width / 2 + 40,
            175,
            320,
            105,
            arcade.color.DARK_GREEN,
        )

        self.draw_tree(350, 210)
        self.draw_tree(635, 210)
        self.draw_tree(505, 235)

        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                245,
                160,
                95,
                22,
            ),
            arcade.color.DARK_BROWN,
        )

        arcade.draw_triangle_filled(
            205,
            171,
            245,
            210,
            245,
            171,
            arcade.color.WOOD_BROWN,
        )

        wave_offset = int(self.time * 40) % 80

        for x in range(-80, width + 80, 80):
            arcade.draw_arc_outline(
                x + wave_offset,
                90,
                55,
                20,
                arcade.color.WHITE,
                0,
                180,
                2,
            )

            arcade.draw_arc_outline(
                x - wave_offset,
                55,
                55,
                20,
                arcade.color.WHITE,
                0,
                180,
                2,
            )

    def draw_tree(self, x, y):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                x,
                y - 25,
                16,
                55,
            ),
            arcade.color.DARK_BROWN,
        )

        arcade.draw_circle_filled(
            x,
            y + 20,
            35,
            arcade.color.DARK_GREEN,
        )

        arcade.draw_circle_filled(
            x - 22,
            y + 5,
            28,
            arcade.color.DARK_GREEN,
        )

        arcade.draw_circle_filled(
            x + 22,
            y + 5,
            28,
            arcade.color.DARK_GREEN,
        )

    def draw_controls_panel(self):
        panel_width = 460
        panel_height = 230

        center_x = self.window.width / 2
        center_y = 140

        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                center_x,
                center_y,
                panel_width,
                panel_height,
            ),
            arcade.color.WHITE,
        )

        arcade.draw_rect_outline(
            arcade.rect.XYWH(
                center_x,
                center_y,
                panel_width,
                panel_height,
            ),
            arcade.color.BLACK,
            3,
        )

        arcade.draw_text(
            "CONTROLS",
            center_x,
            center_y + 75,
            arcade.color.BLACK,
            20,
            anchor_x="center",
        )

        controls_text = [
            "WASD / Arrows - move",
            "E - interact with NPC / well",
            "SPACE - attack",
            "TAB - inventory",
            "M - map",
            "B - build boat",
        ]

        start_y = center_y + 35

        for index, text in enumerate(controls_text):
            arcade.draw_text(
                text,
                center_x - 170,
                start_y - index * 27,
                arcade.color.BLACK,
                14,
            )

    def draw_footer(self):
        arcade.draw_text(
            "2D survival RPG prototype",
            self.window.width / 2,
            25,
            arcade.color.LIGHT_GRAY,
            13,
            anchor_x="center",
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.on_play_click(None)

        elif symbol == arcade.key.ESCAPE:
            if self.show_controls:
                self.show_controls = False
            else:
                arcade.exit()