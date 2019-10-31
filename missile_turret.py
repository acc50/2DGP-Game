from pico2d import *
import game_world

from missile import Missile


class MissileTurret:
    image = None

    def __init__(self, x = 400, y = 300):
        if MissileTurret.image is None:
            MissileTurret.image = load_image('turret-sprite.png')   # 1024  * 1024  8칸씩
        self.x, self.y = x, y
        self.frame_x = 0
        self.frame_y = 3        # 프레임은 0,3 위치가 초기값
        self.attack_timer = 0

    def draw(self):
        self.image.clip_draw(self.frame_x * 124, self.frame_y * 124, 124, 124, self.x, self.y)

    def update(self):
        self.attack_timer += 1
        if self.attack_timer == 500:
            missile = Missile(self.x, self.y, 0, -2)
            game_world.add_object(missile, 1)
            self.attack_timer = 0
