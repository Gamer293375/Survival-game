import arcade
import random

from config import (
    TILE_SCALE,
    UPDATES_PER_FRAME_ENEMY
)

class Enemy:
    APPLE = ":red_apple:"
    WATER = ":droplet:"
    BRONZE_SWORD = "bronze_sword"
    GOLD_SWORD = "gold_sword"

    def __init__(self, x, y, speed=1, health=3, damage_to_player=1):
        self.speed = speed

        self.health = health

        self.damage_to_player = damage_to_player

        self.center_x = x
        self.center_y = y

        self.rad_attack = 50
        self.rad_vision = 150

        self.need_sword = self.BRONZE_SWORD

        self.state = "alive"

        self.reward_item = self.APPLE

    def take_damage(self):
        if self.state == "dead":
            return
        
        self.health -= 1
        if self.health <= 0:
            self.state = "dead"
            self.health = 0

    def get_distance_to_player(self, player_x: float, player_y: float) -> float:
        distance = ((player_x - self.center_x) ** 2 + (player_y - self.center_y) ** 2) ** 0.5
        return distance
    
    def check_attack(self, player_x: int, player_y: int) -> bool:
        distance = self.get_distance_to_player(player_x, player_y)
        return distance <= self.rad_attack
        
    def get_reward_item(self): #тот объект, в который превращается враг после смерти (например яблоко)
        if self.state == "dead":
            return self.reward_item
        return None

    def move(self, player_x: float, player_y: float) -> None: #движение врага (двигаться навстречу игроку, если он находится в определенном диапозоне)
        if self.check_vision(player_x, player_y):
            pass

    def check_vision(self, player_x: float, player_y: float) -> bool: #проверка на то, что игрок находится в диапозоне видимости врага
        distance = self.get_distance_to_player(player_x, player_y)
        return distance <= self.rad_vision
    
    def check_player_sword(self, player_sword: str) -> bool: #проверка на то, что меч игрока подходит для атаки
        if player_sword == self.need_sword:
            return True
        return False
        
    
class EasyEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)


class HardEnemy(Enemy):
    def __init__(self, x, y, speed=1, health=5, damage_to_player=3):
        super().__init__(x, y, speed, health, damage_to_player)

        #self.reward_item *= 2 

        self.rad_vision *= 1.5


class Boss(Enemy):
    def __init__(self, x, y, speed=2, health=12, damage_to_player=4):
        super().__init__(x, y, speed, health, damage_to_player)

        self.reward_item = "" #кусок карты(3)

        self.rad_vision *= 2
        self.rad_attack += 10

        self.need_sword = self.GOLD_SWORD