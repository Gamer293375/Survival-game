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
