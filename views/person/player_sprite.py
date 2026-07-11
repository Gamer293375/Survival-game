import arcade
from config import (
    FRAMES_PER_DIRECTION
)

class PlayerSprite(arcade.Sprite):
    # Возможные направления, куда смотрит игрок.
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    STAY_DOWN = "stay_down"
    STAY_LEFT = "stay_left"
    STAY_RIGHT = "stay_right"
    STAY_UP = "stay_up"
    ATTACK_DOWN = "attack_down"
    ATTACK_LEFT = "attack_left"
    ATTACK_RIGHT = "attack_right"
    ATTACK_UP = "attack_up"

    ATTACK = "attack"
    NOT_ATTACK = "not_attack"

    def __init__(
        self,
        sprite_sheet_path,
        frame_width,
        frame_height,
        frames_per_direction,
        scale=1,
    ):
        # Путь к картинке, где лежат все кадры игрока.
        self.sprite_sheet_path = sprite_sheet_path

        # Размер одного кадра игрока.
        self.frame_width = frame_width
        self.frame_height = frame_height

        # Сколько кадров используется для одного направления.
        self.frames_per_direction = frames_per_direction

        # В начале игрок смотрит вниз.
        self.direction = self.DOWN

        # Номер текущего кадра.
        # Например: 0, 1, 2, потом снова 0.
        self.current_frame = 0

        # Таймер нужен, чтобы кадры менялись не слишком быстро.
        self.animation_timer = 0.0

        # Через сколько секунд переключать кадр.
        self.frame_duration = 0.12

        # Здесь будут храниться кадры для каждого направления.
        self.animation_textures = {
            self.DOWN: [],
            self.LEFT: [],
            self.RIGHT: [],
            self.UP: [],
            self.STAY_DOWN: [],
            self.STAY_LEFT: [],
            self.STAY_RIGHT: [],
            self.STAY_UP: [],
            self.ATTACK_DOWN: [],
            self.ATTACK_LEFT: [],
            self.ATTACK_RIGHT: [],
            self.ATTACK_UP: [],
        }

        # Здесь указываем, в каких строках картинки лежат нужные кадры.
        #
        # Например:
        # строка 3 — игрок идёт вниз,
        # строка 4 — игрок идёт вправо,
        # строка 5 — игрок идёт вверх.
        #
        # Для движения влево отдельной строки нет,
        # поэтому берём строку вправо и потом отражаем её.
        self.direction_rows = {
            self.DOWN: 3,
            self.LEFT: 4,
            self.RIGHT: 4,
            self.UP: 5,
            self.STAY_DOWN: 0,
            self.STAY_LEFT: 1,
            self.STAY_RIGHT: 1,
            self.STAY_UP: 2,
            self.ATTACK_DOWN: 6,
            self.ATTACK_LEFT: 7,
            self.ATTACK_RIGHT: 7,
            self.ATTACK_UP: 8,
        }

        # Вырезаем кадры из общей картинки.
        self.load_animation_textures()

        # Для движения влево берём кадры движения вправо
        # и отражаем их по горизонтали.

        for key in [self.LEFT, self.STAY_LEFT, self.ATTACK_LEFT]:
            self.animation_textures[key] = list(
                map(
                    lambda texture: texture.flip_left_right(),
                    self.animation_textures[key]
                )
            )


        self.animation_on_stay = {
            self.DOWN: self.STAY_DOWN,
            self.RIGHT: self.STAY_RIGHT,
            self.LEFT: self.STAY_LEFT,
            self.UP: self.STAY_UP,
        }

        self.attack_animation = [
            [self.DOWN, self.STAY_DOWN, self.ATTACK_DOWN],
            [self.LEFT, self.STAY_LEFT, self.ATTACK_LEFT],
            [self.RIGHT, self.STAY_RIGHT, self.ATTACK_RIGHT],
            [self.UP, self.STAY_UP, self.ATTACK_UP],
        ]


        # Первый кадр движения вниз ставим как начальную картинку игрока.
        start_texture = self.animation_textures[self.STAY_DOWN][0]

        # Передаём начальную картинку в arcade.Sprite.
        super().__init__(
            start_texture,
            scale=scale,
        )

        self.state = self.NOT_ATTACK

    def load_animation_textures(self):
        # Загружаем общую картинку со всеми кадрами.
        sprite_sheet = arcade.load_spritesheet(self.sprite_sheet_path)

        # Проходим по каждому направлению:
        # вниз, влево, вправо, вверх.
        for direction, row in self.direction_rows.items():

            # В каждой строке берём несколько кадров.
            for frame in range(self.frames_per_direction):

                # Считаем, где начинается нужный кадр по горизонтали.
                x = frame * self.frame_width

                # Считаем, где начинается нужная строка по вертикали.
                y = row * self.frame_height

                # Вырезаем один кадр из общей картинки.
                texture = sprite_sheet.get_texture(
                    arcade.LBWH(
                        x,
                        y,
                        self.frame_width,
                        self.frame_height,
                    )
                )

                # Сохраняем этот кадр в список нужного направления.
                self.animation_textures[direction].append(texture)

    def update_direction(self):
        # Если игрок движется вправо, он смотрит вправо.
        if self.change_x > 0:
            self.direction = self.RIGHT

        # Если игрок движется влево, он смотрит влево.
        elif self.change_x < 0:
            self.direction = self.LEFT

        # Если игрок движется вверх, он смотрит вверх.
        elif self.change_y > 0:
            self.direction = self.UP

        # Если игрок движется вниз, он смотрит вниз.
        elif self.change_y < 0:
            self.direction = self.DOWN

        elif self.change_x == 0 and self.change_y == 0 and self.direction in self.animation_on_stay.keys():
            self.direction = self.animation_on_stay[self.direction]

        for dir in self.attack_animation:
            if (self.direction in (dir[0], dir[1])) and self.state == self.ATTACK:
                self.frames_per_direction = 4
                self.frame_duration = 0.06
                self.direction = dir[2]

    def update_animation(self, delta_time=1 / 60):
        # Сначала обновляем направление игрока.
        self.update_direction()

        # Если игрок двигается, увеличиваем таймер.
        self.animation_timer += delta_time

        # Когда прошло достаточно времени,
        # переключаемся на следующий кадр.
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0.0
            self.current_frame += 1

            # Если кадры закончились, начинаем снова с первого.
            if self.current_frame >= self.frames_per_direction:
                self.current_frame = 0

        # Ставим игроку нужную картинку:
        # берём направление и номер текущего кадра.
        self.texture = self.animation_textures[self.direction][self.current_frame]

        if self.state == self.NOT_ATTACK:
            self.frames_per_direction = FRAMES_PER_DIRECTION
            self.frame_duration = 0.12
            if self.direction == self.ATTACK_DOWN:
                self.direction = self.STAY_DOWN
            elif self.direction == self.ATTACK_LEFT:
                self.direction = self.STAY_LEFT
            elif self.direction == self.ATTACK_RIGHT:
                self.direction = self.STAY_RIGHT
            elif self.direction == self.ATTACK_UP:
                self.direction = self.STAY_UP