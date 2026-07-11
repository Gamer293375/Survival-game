import arcade

import emoji 

from .person.player import Player

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

        self.equipment_pressed = False

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.attack = False

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

        self.player = Player(200, 500, PLAYER_SPEED)

        self.player_list.append(self.player.sprite)

        self.wall_list = self.create_wall_list()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player.sprite,
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
            arcade.color.BLACK,
            16,
        )
        bar_list = [
            ("Food:", ':red_apple:', arcade.color.RED, self.player.food_health),
            ("Water:", ':droplet:', arcade.color.BLUE, self.player.water_health),
            ("Air:", ':bubbles:', arcade.color.WHITE, self.player.air_health)
        ]
        for i in range(len(bar_list)):
            arcade.draw_text(
                f"{bar_list[i][0]} {emoji.emojize(bar_list[i][1]) * bar_list[i][3]}",
                20,
                50 + i * 30,
                bar_list[i][2],
                15
            )  

        if self.equipment_pressed:
            self.draw_equipment_panel()

    def draw_equipment_panel(self):
        panel_width = 350
        panel_height = 350

        center_x = self.window.width / 2
        center_y = self.window.height / 2

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
            "EQUIPMENT",
            center_x,
            center_y + 75,
            arcade.color.BLACK,
            20,
            anchor_x="center",
        )

        start_y = center_y + 35

        for index, (name, amount) in enumerate(self.player.equipment.get_items()):
            arcade.draw_text(
                f"{name}: {amount}",
                center_x - 170,
                start_y - index * 27,
                arcade.color.BLACK,
                14,
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

        self.player.sprite.update_animation()
        
        self.player.update_food_and_water(delta_time)

        self.player.update_air(delta_time)

        self.update_camera()

        self.update_animated_layers(delta_time)

    def update_player_movement(self):
        self.player.move(
            self.left_pressed,
            self.right_pressed,
            self.up_pressed,
            self.down_pressed
        )

    def update_camera(self):
        self.camera.position = self.player.sprite.position

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

        elif symbol == arcade.key.TAB:
            self.equipment_pressed = not self.equipment_pressed
        
        elif symbol == arcade.key.E:
            self.player.take_item("food")
        
        elif symbol == arcade.key.G:
            self.player.eat()

        elif symbol == arcade.key.SPACE:
            self.player.attack()

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.left_pressed = False

        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.right_pressed = False

        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            self.up_pressed = False

        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.down_pressed = False

        elif symbol == arcade.key.SPACE:
            self.player.not_attack()