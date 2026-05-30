import arcade
import arcade.gui

from .game import GameView

class MenuView(arcade.View):
    def __init__(self, main_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        title = arcade.gui.UILabel("PLATFORMER", font_size=40)
        lvl1 = arcade.gui.UIFlatButton(text="play", width=50)
        lvl1.on_click = self.lvl

        self.grid = arcade.gui.UIGridLayout(
            column_count=3, row_count=2, horizontal_spacing=20
        )
        self.grid.add(title, column=0, row=0, column_span=3)
        self.grid.add(lvl1, column=0, row=1)

        self.archor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.archor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid
        )
        self.main_view = main_view
    
    def lvl(self, event):
        game = GameView()
        game.setup()
        self.main_view.show_view(game)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()