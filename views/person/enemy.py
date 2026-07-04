import arcade
import random

from config import (
    TILE_SCALE,
    UPDATES_PER_FRAME_ENEMY
)

class Enemy:
    APPLE = ""
    WATER = ""
    AIR = ""

    def __init__(self):
        self.speed = 1

        self.health = 3

        self.damage_to_player = 1

        self.center_x = random.randint()
        self.center_y = random.randint()

        self.scale = TILE_SCALE

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.state = "dead"
            self.health = 0

    def check_attack(self, player_x: int, player_y: int) -> bool:
        player_coords = []
        for player_x_coord in range(player_x - 10, player_x + 10):
            player_coords.append(player_x_coord)
        for player_y_coord in range(player_y - 10, player_y + 10):
            player_coords.append(player_y_coord)
        if self.center_x in player_coords and self.center_y in player_coords:
            return True
        
    def object_after_dead(self, object: str): #тот объект, в который превращается враг после смерти (например яблоко или кусок мяса)
        pass

    def move(self): #движение врага (двигаться навстречу игроку, если он находится в определенном диапозоне)
        if self.check_range:
            pass

    def check_range(self, player_x: int, range: list) -> bool: #проверка на то, что игрок находится в диапозоне видимости врага
        if player_x in range:
            return True
    
    def check_player_sword(self, need_sword: str, player_sword: str) -> bool: #проверка на то, что меч игрока подходит для атаки
        if player_sword == need_sword:
            return True
        
    
class EasyEnemy(Enemy):
    def __init__(self):
        super().__init__()

        self.health += 2

        self.damage_to_player += 2

