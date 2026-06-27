import arcade

from .equipment import Equipment
from .player_sprite import PlayerSprite

class Player:

    def __init__(self, x, y, speed):

        self.speed = speed

        self.sprite = PlayerSprite(
            sprite_sheet_path="assets/player/player.png",
            frame_width=48,
            frame_height=48,
            frames_per_direction=6,
            scale=1,
        )

        self.sprite.center_x = x
        self.sprite.center_y = y

        self.food_health = 5
        self.water_health = 5

        self.air_health = 5

        self.max_health = 5

        self.food_and_water_timer = 0
        self.air_timer = 0

        self.equipment = Equipment()

    def move(self, left, right, up, down):
        self.sprite.change_x = 0
        self.sprite.change_y = 0

        if left:
            self.sprite.change_x = -self.speed
        elif right:
            self.sprite.change_x = self.speed

        if up:
            self.sprite.change_y = self.speed
        elif down:
            self.sprite.change_y = -self.speed

    def update_food_and_water(self, delta_time):
        self.food_and_water_timer += delta_time
        if self.food_and_water_timer >= 30:
            self.food_health -= 1
            self.water_health -= 1
            self.food_and_water_timer = 0
            self.check_game_over()

    def update_air(self, delta_time): #under water
        self.air_timer += delta_time
        if self.air_timer >= 5:
            self.air_health -= 1
            self.air_timer = 0
            self.check_game_over()

    def eat(self):
        if not self.equipment.has_item("food"):
            return "You don't have any food"
        
        if self.food_health == self.max_health:
            return "Your food bar is already full"
        
        self.food_health += 1
        self.equipment.remove_item("food")
        return None

    def drink(self):
        if not self.equipment.has_item("water"):
            return "You don't have any water"
        
        if self.water_health == self.max_health:
            return "Your water bar is already full"
        
        self.water_health += 1
        self.equipment.remove_item("water")

    def check_game_over(self):
        if self.water_health == 0 or self.food_health == 0 or self.air_health == 0:
            pass
    
    def take_item(self, item_name, amount=1):

        self.equipment.add_item(item_name, amount)

        print(f"вы подняли {item_name} - {amount}")