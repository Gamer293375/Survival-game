import arcade

class Player:

    def __init__(self, x, y, speed):

        self.speed = speed

        self.sprite = arcade.SpriteSolidColor(
            width=16,
            height=16,
            color=arcade.color.BLUE,
        )

        self.sprite.center_x = x
        self.sprite.center_y = y

        self.food_health = 5
        self.water_health = 5

        self.air_health = 5

        self.max_health = 5

        self.food_and_water_timer = 0
        self.air_timer = 0

        self.equipment = {
            "food": 1,
            "water": 1,
            "sword": 1,
            "hammer": 0,
            "saw": 0,
            "map_piece": 0
        }

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
        if self.air_timer >= 20:
            self.air_health -= 1
            self.air_timer = 0
            self.check_game_over()

    def eat(self):
        if self.equipment["food"] == 0:
            return "You don't have any food"
        if self.food_health == self.max_health:
            return "Your food bar is already full"
        self.food_health += 1
        self.equipment["food"] -= 1
        return None

    def drink(self):
        if self.equipment["water"] == 0:
            return "You don't have any water"
        if self.water_health == self.max_health:
            return "Your water bar is already full"
        self.water_health += 1
        self.equipment["water"] -= 1

    def check_game_over(self):
        if self.water_health == 0 or self.food_health == 0 or self.air_health == 0:
            pass