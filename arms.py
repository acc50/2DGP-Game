from pico2d import *
import game_world

UP, DOWN, RIGHT, LEFT = range(4)

INFINITE = 1000


class Arms:
    def __init__(self, x=400, y=300, velocity_x=1, velocity_y=1):
        self.x, self.y = x, y
        self.shoot_dir = RIGHT

    def draw(self):
        if self.shoot_dir is UP:
            pass
        elif self.shoot_dir is DOWN:
            pass
        elif self.shoot_dir is RIGHT:
            pass
        elif self.shoot_dir is LEFT:
            pass

    def update(self):
        # 플레이어의 view_dir 을 받아와 방향 설정
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x < -100 or self.x > 900:
            game_world.remove_object(self)


class Spur(Arms):  # 레이저
    arm_image = None
    bullet_image = None

    def __init__(self):
        if Spur.arm_image is None:
            Spur.arm_image = load_image('Spur.png')     # 24 * 97

        self.level = 1
        self.MAX_BULLETS = INFINITE
        self.MAX_EXP = [30, 50, 100]
        self.damages = [7, 30, 70]  # 차지x, 1단계, 2단계
        self.current_exp = 0
        self.current_bullets = 0
        self.MAX_SHOOT_COUNT = INFINITE     # 최대 연사 수
        self.range = 100

        pass

    def shoot(self):
        if self.shoot_dir is UP:
            pass
        elif self.shoot_dir is DOWN:
            pass
        elif self.shoot_dir is RIGHT:
            pass
        elif self.shoot_dir is LEFT:
            pass


class MissileLauncher(Arms):
    arm_image = None
    bullet_image = None

    def __init__(self):
        if MissileLauncher.arm_image is None:
            MissileLauncher.arm_image = load_image('MissileLauncher.png')   # 30 * 100

        self.level = 1
        self.MAX_BULLETS = 30
        self.MAX_EXP = [20, 40, 60]
        self.damages = [20, 30, 50]  # 1레벨, 2레벨, 3레벨
        self.current_exp = 0
        self.current_bullets = 0
        self.MAX_SHOOT_COUNT = 1    # 최대 연사 수
        self.range = 100

        pass

    def shoot(self):
        if self.shoot_dir is UP:
            pass
        elif self.shoot_dir is DOWN:
            pass
        elif self.shoot_dir is RIGHT:
            pass
        elif self.shoot_dir is LEFT:
            pass


class Blade(Arms):
    arm_image = None

    def __init__(self):
        if Blade.arm_image is None:
            Blade.arm_image = load_image('Spur.png')

        self.level = 1
        self.MAX_BULLETS = INFINITE
        self.MAX_EXP = [20, 40, 60]
        self.damages = [15, 18, 30]  # 1레벨, 2레벨, 3레벨        거리에 따른 데미지 차이 있음
        self.current_exp = 0
        self.current_bullets = 0
        self.MAX_SHOOT_COUNT = 1    # 최대 연사 수
        self.range = 100

        pass

    def shoot(self):
        if self.shoot_dir is UP:
            pass
        elif self.shoot_dir is DOWN:
            pass
        elif self.shoot_dir is RIGHT:
            pass
        elif self.shoot_dir is LEFT:
            pass

    def draw(self): # 공격시만 무기가 보이므로 따로 그림
        pass


class Nemesis(Arms):
    arm_image = None

    def __init__(self):
        if Nemesis.arm_image is None:
            Nemesis.arm_image = load_image('Spur.png')

        self.level = 1
        self.MAX_BULLETS = 30
        self.MAX_EXP = [10, 5, 1]
        self.damages = [12, 8, 1]  # 1레벨, 2레벨, 3레벨
        self.current_exp = 0
        self.current_bullets = 0
        self.MAX_SHOOT_COUNT = 1    # 최대 연사 수
        self.range = 500

        pass

    def shoot(self):
        if self.shoot_dir is UP:
            pass
        elif self.shoot_dir is DOWN:
            pass
        elif self.shoot_dir is RIGHT:
            pass
        elif self.shoot_dir is LEFT:
            pass

