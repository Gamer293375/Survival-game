import arcade


class PlayerSprite(arcade.Sprite):
    # Возможные направления, куда смотрит игрок.
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"

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
        }

        # Вырезаем кадры из общей картинки.
        self.load_animation_textures()

        # Для движения влево берём кадры движения вправо
        # и отражаем их по горизонтали.
        self.animation_textures[self.LEFT] = list(
            map(
                lambda texture: texture.flip_left_right(),
                self.animation_textures[self.LEFT]
            )
        )

        # Первый кадр движения вниз ставим как начальную картинку игрока.
        start_texture = self.animation_textures[self.DOWN][0]

        # Передаём начальную картинку в arcade.Sprite.
        super().__init__(
            start_texture,
            scale=scale,
        )

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

    def update_animation(self, delta_time=1 / 60):
        # Сначала обновляем направление игрока.
        self.update_direction()

        # Проверяем, двигается ли игрок.
        is_moving = (
            self.change_x != 0
            or self.change_y != 0
        )

        # Если игрок стоит на месте,
        # показываем первый кадр текущего направления.
        if not is_moving:
            self.current_frame = 0
            self.animation_timer = 0.0
            self.texture = self.animation_textures[self.direction][0]
            return

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