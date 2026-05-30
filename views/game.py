import arcade

from config import (
    TILE_SCALE,
    PLAYER_SCALE,
)

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def load_sprite_lists(self):
        # self.player_list = arcade.SpriteList()
        # self.enemy_list = arcade.SpriteList()
        self.water_list = self.tile_map.sprite_lists["Water"]
        self.road_list = self.tile_map.sprite_lists["Road"]


    def setup(self):
        self.tile_map = arcade.load_tilemap(
            "assets/maps/Main.tmx",
            # scaling=TILE_SCALE,
        )
        self.load_sprite_lists()

    def on_draw(self):
        self.clear()
        self.water_list.draw()
        self.road_list.draw()

    def on_update(self, delta_time):
        self.water_list.update_animation(delta_time)
    
    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass