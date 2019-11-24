from pico2d import *

import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
BULLET_SPEED_KMPH = 110.0  # 110 Km / Hour
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

UP, DOWN, RIGHT, LEFT = range(4)


class SpurBullet:
    image = None

    def __init__(self, x, y, shoot_dir, gun_range, gun_level):
        if self.image is None:
            self.image = load_image('./Image/Arms/Bullet.png')      # 320 * 176

        self.x, self.y = x, y
        self.shoot_point = x, y

        self.frame_x, self.frame_y = 0, 0
        self.size_x, self.size_y = 0, 0
        self.level = gun_level

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
            self.size_x = 7
            self.size_y = 16
        elif shoot_dir is LEFT:
            self.frame_x = 184
            self.frame_y = 68
            self.size_x = 16
            self.size_y = 7

        self.dir = shoot_dir
        self.range = gun_range

    def draw(self):
        self.image.clip_draw(self.frame_x, self.frame_y, self.size_x, self.size_y, self.x, self.y)

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
            game_world.remove_object(self)
            pass


class MissileBullet:
    image = None

    def __init__(self, x, y, shoot_dir, gun_range, gun_level):      # 총의 위치, 방향, 사거리, 레벨
        if self.image is None:
            self.image = load_image('./Image/Arms/Bullet.png')      # 320 * 176

        self.x, self.y = x, y
        self.shoot_point = x, y

        self.frame_x, self.frame_y = 0, 0
        self.size_x, self.size_y = 0, 0
        self.level = gun_level

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

        self.dir = shoot_dir
        self.range = gun_range

    def draw(self):
        self.image.clip_draw(self.frame_x, self.frame_y, self.size_x, self.size_y, self.x, self.y, self.size_x * 2, \
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
            game_world.remove_object(self)

