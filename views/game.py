import arcade

from config import (
    PLAYER_SPEED,
    TILE_SCALE,
)


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.tile_map = None

        self.player = None
        self.player_list = None

        self.wall_list = None
        self.physics_engine = None

        self.camera = None
        self.gui_camera = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.map_layers = [
            "Ground",
            "Flowers",
            "Road",
            "Shadows",
            "Object Shadows",
            "RockSlopes",
            "RockSlopes_Auto",
            "Water",
            "Object Layer 1",
        ]

        self.collision_layers = [
            # "Water",
            # "RockSlopes",
            # "RockSlopes_Auto",
            "Object Layer 1",
        ]

    def setup(self):
        self.tile_map = arcade.load_tilemap(
            "assets/maps/Main.tmx",
            scaling=TILE_SCALE,
        )

        self.setup_shadow_layers()

        self.player_list = arcade.SpriteList()

        self.player = arcade.SpriteSolidColor(
            width=16,
            height=16,
            color=arcade.color.BLUE,
        )

        self.player.center_x = 200
        self.player.center_y = 500

        self.player_list.append(self.player)

        self.wall_list = self.create_wall_list()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.wall_list,
        )

        self.camera = arcade.Camera2D(zoom=2)
        self.gui_camera = arcade.Camera2D()

    def setup_shadow_layers(self):
        shadow_layers = [
            "Shadows",
            "Object Shadows",
        ]

        for layer_name in shadow_layers:
            if layer_name in self.tile_map.sprite_lists:
                for sprite in self.tile_map.sprite_lists[layer_name]:
                    sprite.alpha = 50

    def create_wall_list(self):
        wall_list = arcade.SpriteList()

        for layer_name in self.collision_layers:
            if layer_name in self.tile_map.sprite_lists:
                for sprite in self.tile_map.sprite_lists[layer_name]:
                    wall_list.append(sprite)

        return wall_list

    def draw_map(self):
        for layer_name in self.map_layers:
            if layer_name in self.tile_map.sprite_lists:
                self.tile_map.sprite_lists[layer_name].draw()

    def draw_ui(self):
        arcade.draw_text(
            "WASD / arrows - move",
            20,
            20,
            arcade.color.WHITE,
            16,
        )

    def on_draw(self):
        self.clear()

        with self.camera.activate():
            self.draw_map()
            self.player_list.draw()

        with self.gui_camera.activate():
            self.draw_ui()

    def on_update(self, delta_time):
        self.update_player_movement()

        self.physics_engine.update()

        self.update_camera()

        self.update_animated_layers(delta_time)

    def update_player_movement(self):
        self.player.change_x = 0
        self.player.change_y = 0

        if self.left_pressed:
            self.player.change_x = -PLAYER_SPEED
        elif self.right_pressed:
            self.player.change_x = PLAYER_SPEED

        if self.up_pressed:
            self.player.change_y = PLAYER_SPEED
        elif self.down_pressed:
            self.player.change_y = -PLAYER_SPEED

    def update_camera(self):
        self.camera.position = self.player.position

    def update_animated_layers(self, delta_time):
        animated_layers = [
            "Water",
            "Flowers",
        ]

        for layer_name in animated_layers:
            if layer_name in self.tile_map.sprite_lists:
                self.tile_map.sprite_lists[layer_name].update_animation(delta_time)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.left_pressed = True

        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.right_pressed = True

        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            self.up_pressed = True

        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.left_pressed = False

        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.right_pressed = False

        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            self.up_pressed = False

        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.down_pressed = False