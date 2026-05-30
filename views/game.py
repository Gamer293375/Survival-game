import arcade

from config import (
    TILE_SCALE,
    PLAYER_SCALE,
)

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)
    
    def setup(self):
        pass

    def on_draw(self):
        self.clear()
    
    def on_update(self, delta_time):
        pass
    
    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass