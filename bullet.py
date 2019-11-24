from pico2d import *

import game_world
import game_framework
import main_state

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
BULLET_SPEED_KMPH = 110.0  # 110 Km / Hour
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

UP, DOWN, RIGHT, LEFT = range(4)


class SpurBullet:
    image = None

    def __init__(self, x, y, shoot_dir, arm_range, arm_level):
        if self.image is None:
            self.image = load_image('./Image/Arms/Bullet.png')      # 320 * 176

        self.x, self.y = x, y
        self.shoot_point = x, y

        self.frame_x, self.frame_y = 0, 0
        self.size_x, self.size_y = 0, 0
        self.level = arm_level

        self.dir = shoot_dir
        self.range = arm_range

        if arm_level is 1:
            if (shoot_dir is UP) or (shoot_dir is DOWN):
                self.frame_x = 151
                self.frame_y = 130
                self.size_x = 2
                self.size_y = 12
            elif (shoot_dir is LEFT) or (shoot_dir is RIGHT):
                self.frame_x = 130
                self.frame_y = 135
                self.size_x = 12
                self.size_y = 2

        if arm_level is 2:
            if (shoot_dir is UP) or (shoot_dir is DOWN):        # 176
                self.frame_x = 182
                self.frame_y = 130
                self.size_x = 4
                self.size_y = 12
            elif (shoot_dir is LEFT) or (shoot_dir is RIGHT):
                self.frame_x = 162
                self.frame_y = 134
                self.size_x = 12
                self.size_y = 4
            pass

        elif arm_level is 3:
            if (shoot_dir is UP) or (shoot_dir is DOWN):        # 176
                self.frame_x = 148
                self.frame_y = 112
                self.size_x = 8
                self.size_y = 16
            elif (shoot_dir is LEFT) or (shoot_dir is RIGHT):
                self.frame_x = 128
                self.frame_y = 116
                self.size_x = 16
                self.size_y = 8
            pass

    def draw(self):
        self.image.clip_draw(self.frame_x, self.frame_y, self.size_x, self.size_y, self.x, self.y, 50, 50)

    def update(self):
        if self.dir is UP:
            self.y += BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is DOWN:
            self.y -= BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is RIGHT:
            self.x += BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is LEFT:
            self.x -= BULLET_SPEED_PPS * game_framework.frame_time

        if (self.shoot_point[0] - self.x)**2 + (self.shoot_point[1] - self.y)**2 > self.range**2:
            player = main_state.get_player()
            player.arms[player.current_arm].bullets.remove(self)
            game_world.remove_object(self)
            pass


class MissileBullet:
    image = None

    def __init__(self, x, y, shoot_dir, arm_range, arm_level):      # 총의 위치, 방향, 사거리, 레벨
        if self.image is None:
            self.image = load_image('./Image/Arms/Bullet.png')      # 320 * 176

        self.x, self.y = x, y
        self.shoot_point = x, y

        self.frame_x, self.frame_y = 0, 0
        self.size_x, self.size_y = 0, 0
        self.level = arm_level

        self.dir = shoot_dir
        self.range = arm_range

        if shoot_dir is UP:
            self.frame_x = 205
            self.frame_y = 64
            self.size_x = 7
            self.size_y = 16
        elif shoot_dir is DOWN:
            self.frame_x = 237
            self.frame_y = 64
            self.size_x = 7
            self.size_y = 16
        elif shoot_dir is RIGHT:
            self.frame_x = 216
            self.frame_y = 68
            self.size_x = 16
            self.size_y = 7
        elif shoot_dir is LEFT:
            self.frame_x = 184
            self.frame_y = 68
            self.size_x = 16
            self.size_y = 7

    def draw(self):
        self.image.clip_draw(self.frame_x, self.frame_y, self.size_x, self.size_y, self.x, self.y, self.size_x * 2,
                             self.size_y * 2)

    def update(self):
        if self.dir is UP:
            self.y += BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is DOWN:
            self.y -= BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is RIGHT:
            self.x += BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is LEFT:
            self.x -= BULLET_SPEED_PPS * game_framework.frame_time

        if (self.shoot_point[0] - self.x)**2 + (self.shoot_point[1] - self.y)**2 > self.range**2:
            player = main_state.get_player()
            player.arms[player.current_arm].bullets.remove(self)
            game_world.remove_object(self)


class BladeAttack:
    image = None

    def __init__(self, x, y, shoot_dir, arm_range, arm_level):      # 총의 위치, 방향, 사거리, 레벨
        if self.image is None:
            self.image = load_image('./Image/Arms/Bullet.png')      # 320 * 176

        self.x, self.y = x, y
        self.shoot_point = x, y

        self.frame_x, self.frame_y = 0, 113
        self.size_x, self.size_y = 16, 14
        self.level = arm_level

        self.dir = shoot_dir
        self.range = arm_range

    def draw(self):
        self.image.clip_draw(self.frame_x * self.size_x, self.frame_y, self.size_x, self.size_y, self.x, self.y,
                             self.size_x * 2, self.size_y * 2)

    def update(self):
        if self.dir is UP:
            self.y += BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is DOWN:
            self.y -= BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is RIGHT:
            self.x += BULLET_SPEED_PPS * game_framework.frame_time
        elif self.dir is LEFT:
            self.x -= BULLET_SPEED_PPS * game_framework.frame_time

        self.frame_x = (self.frame_x + 1) % 8

        if (self.shoot_point[0] - self.x)**2 + (self.shoot_point[1] - self.y)**2 > self.range**2:
            player = main_state.get_player()
            player.arms[player.current_arm].bullets.remove(self)
            game_world.remove_object(self)


class NemesisBullet:
    image = None

    def __init__(self, x, y, shoot_dir, arm_range, arm_level):      # 총의 위치, 방향, 사거리, 레벨
        if self.image is None:
            self.image = load_image('./Image/Arms/Bullet.png')      # 32*32  2등분

        self.x, self.y = x, y
        self.shoot_point = x, y

        self.frame_x, self.frame_y = 0, 0
        self.size_x, self.size_y = 0, 0
        self.change_color = 0

        self.level = arm_level
        self.dir = shoot_dir
        self.range = arm_range
        self.speed_ratio = 1.7

        if shoot_dir is UP:
            self.frame_x = 32
            self.frame_y = 32
            self.size_x = 16
            self.size_y = 32
        elif shoot_dir is DOWN:
            self.frame_x = 96
            self.frame_y = 32
            self.size_x = 16
            self.size_y = 32
        elif shoot_dir is RIGHT:
            self.frame_x = 64
            self.frame_y = 32
            self.size_x = 32
            self.size_y = 16
        elif shoot_dir is LEFT:
            self.frame_x = 0
            self.frame_y = 32
            self.size_x = 32
            self.size_y = 16

        if arm_level is 2:
            self.frame_x += 128
            self.range = 350
            self.speed_ratio = 1.2

        if arm_level is 3:
            self.frame_y -= 32
            self.range = 200
            self.speed_ratio = 0.5

    def draw(self):
        if (self.dir is LEFT) or (self.dir is RIGHT):
            self.image.clip_draw(self.frame_x, self.frame_y + 16 * self.change_color, self.size_x, self.size_y, self.x,
                                 self.y, self.size_x * 3, self.size_y * 2)
        else:
            self.image.clip_draw(self.frame_x + 16 * self.change_color, self.frame_y, self.size_x, self.size_y, self.x,
                                 self.y, self.size_x * 2, self.size_y * 3)

    def update(self):
        if self.dir is UP:
            self.y += BULLET_SPEED_PPS * self.speed_ratio * game_framework.frame_time
        elif self.dir is DOWN:
            self.y -= BULLET_SPEED_PPS * self.speed_ratio * game_framework.frame_time
        elif self.dir is RIGHT:
            self.x += BULLET_SPEED_PPS * self.speed_ratio * game_framework.frame_time
        elif self.dir is LEFT:
            self.x -= BULLET_SPEED_PPS * self.speed_ratio * game_framework.frame_time

        self.change_color = (self.change_color + 1) % 2

        if (self.shoot_point[0] - self.x)**2 + (self.shoot_point[1] - self.y)**2 > self.range**2:
            player = main_state.get_player()
            player.arms[player.current_arm].bullets.remove(self)
            game_world.remove_object(self)

