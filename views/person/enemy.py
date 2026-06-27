import arcade
import random

from config import (
    TILE_SCALE,
    UPDATES_PER_FRAME_ENEMY
)

class Enemy:
    def __init__(self, damage):
        self.speed = 1

        self.health = random.choice([3, 5])

        self.damage_to_player = damage

        self.center_x = random.randint()
        self.center_y = random.randint()

        self.cur_texture = 0

        self.state = "walk"

        img_path = ""

        self.walk_textures = []
        self.texture = self.walk_textures[][]

        self.special_textures = []

        self.dead_time = 0
        self.attack_time = 0

        self.scale = TILE_SCALE

    def update_enemy(self, delta_time = 1 / 60):
        if self.state == "dead":
            self.dead_time += 1
            return
        

    def update_animation(self, delta_time = 1 / 60):
        if self.state == "dead":
            self.texture = self.special_textures[][]
            if self.dead_time == 150:
                self.remove_from_sprite_lists()
            return
        
        elif self.state == "attack":
            self.attack_time += 1
            if self.attack_time == 10:
                self.state = "walk"
                self.attack_time = 0
            self.texture = self.special_textures
            return

        else:
            self.cur_texture += 1
            if self.cur_texture >= 2 * UPDATES_PER_FRAME_ENEMY:
                self.cur_texture = 0
            
            frame = self.cur_texture // UPDATES_PER_FRAME_ENEMY
            self.texture = self.walk_textures[][]            
            return

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.state = "dead"
            self.health = 0

    def check_attack(self, player_x: int, player_y: int) -> bool:
        pass