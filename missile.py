from pico2d import *
import game_world


class Missile:
    image = None

    def __init__(self, x=400, y=300, velocity_x=1, velocity_y=1):
        if Missile.image is None:
            Missile.image = load_image('missile.png')  # 253 * 178
        self.x, self.y = x, y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def draw(self):
        self.image.clip_composite_draw(0, 0, 253, 178,
                                       -3.141592 / 2, '', self.x - 10, self.y - 25, 40, 40)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x < -100 or self.x > 900:
            game_world.remove_object(self)
