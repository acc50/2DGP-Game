from pico2d import *
import game_world
import random


class Boost:
    image = None

    def __init__(self, x=1, y=1, velocity_x=1, velocity_y=1):
        if Boost.image is None:
            Boost.image = load_image('./Image/Effect/Boost.png')  # 8*8 7프레임

        rand = random.randint(-10, 10)
        self.x, self.y = x, y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        if velocity_x != 0:
            self.x += rand
            self.velocity_x += (rand / 10)
        elif velocity_y != 0:
            self.y += rand
            self.velocity_y += (rand / 10)
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 8, 0, 8, 8, self.x, self.y, 20, 20)

    def update(self):
        self.x += self.velocity_x * 1.5
        self.y += self.velocity_y * 1.5
        self.frame += 1

        if self.frame > 7:
            game_world.remove_object(self)
