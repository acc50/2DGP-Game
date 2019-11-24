from pico2d import *

import game_world
from bullet import SpurBullet, MissileBullet, BladeAttack, NemesisBullet

UP, DOWN, RIGHT, LEFT = range(4)

INFINITE = 1000


class Arms:
    arm_image = None
    bullet_image = None

    def __init__(self):
        self.x, self.y = 400, 300
        self.shoot_dir = RIGHT
        self.player_move_dir = 0

        self.frame_x, self.frame_y = 0, 0
        self.frame_size_x = 0
        self.frame_size_y = 0

    def draw(self):
        self.arm_image.clip_draw(self.frame_x, self.frame_y, self.frame_size_x, self.frame_size_y, self.x, self.y, 30, 30)

    def synchronize_to_player(self, player_view_dir_y, player_view_dir_x, x, y):
        if player_view_dir_y > 0:
            self.shoot_dir = UP
        else:
            if player_view_dir_x > 0:
                self.shoot_dir = RIGHT
            else:
                self.shoot_dir = LEFT
        self.player_move_dir = player_view_dir_x
        # self.shoot_dir = player_view_dir
        # self.player_move_dir = player_view_dir_y
        self.x, self.y = x, y

        pass


class Spur(Arms):  # 레이저
    arm_image = None

    def __init__(self):
        if Spur.arm_image is None:
            Spur.arm_image = load_image('./Image/Arms/Spur.png')     # 24 * 97 , 9*9 size

        self.level = 1
        self.MAX_BULLETS = INFINITE
        self.MAX_EXP = [30, 100, 230]
        self.damages = [7, 30, 70]  # 차지x, 1단계, 2단계
        self.current_exp = 0
        self.current_damage = 7
        self.current_bullets = 0
        self.max_shoot_count = INFINITE     # 최대 연사 수
        self.range = 100

        self.frame_x = 0
        self.frame_y = 0
        self.frame_size_x = 9     # 9*9 size
        self.frame_size_y = 9
        self.shoot_dir = RIGHT
        self.bullets = []

        self.is_charge = False
        self.is_level_max = False
        self.is_level_min = True

        self.x, self.y, self.move_dir = 400, 300, RIGHT
        pass

    def update(self):
        if self.shoot_dir is UP:
            if self.player_move_dir is LEFT:
                self.frame_x = 8
                self.frame_y = 62
            elif self.player_move_dir is RIGHT:
                self.frame_x = 7
                self.frame_y = 46
            pass
        elif self.shoot_dir is DOWN:
            if self.player_move_dir is LEFT:
                self.frame_x = 10
                self.frame_y = 25
            elif self.player_move_dir is RIGHT:
                self.frame_x = 4
                self.frame_y = 9
            pass
        elif self.shoot_dir is RIGHT:
            self.frame_x = 10
            self.frame_y = 71
            pass
        elif self.shoot_dir is LEFT:
            self.frame_x = 5
            self.frame_y = 87
            pass

        # 레벨 증가
        if self.is_charge and not self.is_level_max:
            self.current_exp += 0.2
        elif not self.is_charge:
            self.current_exp = 0
            self.is_level_max = False
            self.is_level_min = True
            self.level = 1

        if self.is_level_min and self.current_exp > 0:  # 1레벨, 경험치 0이었는데 증가시
            self.is_level_min = False

        if (self.level is 3) and (not self.is_level_max):
            if self.current_exp >= self.MAX_EXP[self.level - 1]:
                self.current_exp = self.MAX_EXP[self.level - 1]
                self.is_level_max = True
            pass
        elif (self.level is 1) or (self.level is 2):
            if self.current_exp > self.MAX_EXP[self.level - 1]:
                self.current_exp -= self.MAX_EXP[self.level - 1]
                self.level += 1

        # 레벨 감소
        if self.is_level_max and (self.current_exp is not self.MAX_EXP[self.level - 1]):    # MAX 이고, 경험치가 MAX 는 아니면
            self.is_level_max = False
            
        elif self.level > 1:
            if self.current_exp < 0:        # 레벨 감소 발생
                self.level -= 1
                self.current_exp = self.MAX_EXP[self.level - 1] + self.current_exp      # current_exp 는 음수 이므로 +

        elif (self.current_exp <= 0) and (not self.is_level_min):     # 1레벨에서 경험치가 전부 사라지면
            self.current_exp = 0
            self.is_level_min = True
            pass

        print(self.level, ' and ', self.current_exp)


    def shoot(self):
        if len(self.bullets) < self.max_shoot_count:
            bullet = SpurBullet(self.x, self.y, self.shoot_dir, self.range, self.level)
            game_world.add_object(bullet, 1)

            self.bullets.append(bullet)


class MissileLauncher(Arms):
    arm_image = None

    def __init__(self):
        if MissileLauncher.arm_image is None:
            MissileLauncher.arm_image = load_image('./Image/Arms/MissileLauncher.png')   # 30 * 100

        self.level = 1
        self.MAX_BULLETS = 30
        self.MAX_EXP = [20, 40, 60]
        self.damages = [20, 30, 50]  # 1레벨, 2레벨, 3레벨
        self.current_exp = 0
        self.current_bullets = 0
        self.max_shoot_count = 1    # 최대 연사 수
        self.range = 270

        self.frame_x = 0
        self.frame_y = 0
        self.frame_size_x = 0
        self.frame_size_y = 0
        self.shoot_dir = RIGHT
        self.bullets = []

        self.is_level_max = False
        self.is_level_min = False

        self.x, self.y, self.move_dir = 400, 300, RIGHT
        pass

    def update(self):
        if self.shoot_dir is UP:
            self.frame_size_x = 10
            self.frame_size_y = 15

            if self.player_move_dir is LEFT:
                self.frame_x = 10
                self.frame_y = 52
            elif self.player_move_dir is RIGHT:
                self.frame_x = 10
                self.frame_y = 36

        elif self.shoot_dir is DOWN:
            self.frame_size_x = 10
            self.frame_size_y = 15

            if self.player_move_dir is LEFT:
                self.frame_x = 14
                self.frame_y = 21
            elif self.player_move_dir is RIGHT:
                self.frame_x = 6
                self.frame_y = 5

        elif self.shoot_dir is LEFT:        # y = 100
            self.frame_size_x = 22
            self.frame_size_y = 12
            self.frame_x = 6
            self.frame_y = 84

        elif self.shoot_dir is RIGHT:
            self.frame_size_x = 22
            self.frame_size_y = 12
            self.frame_x = 2
            self.frame_y = 68

        # 레벨 증가
        if self.is_level_min and self.current_exp > 0:  # 1레벨, 경험치 0이었는데 증가시
            self.is_level_min = False

        if (self.level is 3) and (not self.is_level_max):
            if self.current_exp >= self.MAX_EXP[self.level - 1]:
                self.current_exp = self.MAX_EXP[self.level - 1]
                self.is_level_max = True
            pass
        elif (self.level is 1) or (self.level is 2):
            if self.current_exp > self.MAX_EXP[self.level - 1]:
                self.current_exp -= self.MAX_EXP[self.level - 1]
                self.level += 1

        # 레벨 감소
        if self.is_level_max and (self.current_exp is not self.MAX_EXP[self.level - 1]):  # MAX 이고, 경험치가 MAX 는 아니면
            self.is_level_max = False

        elif self.level > 1:
            if self.current_exp < 0:  # 레벨 감소 발생
                self.level -= 1
                self.current_exp = self.MAX_EXP[self.level - 1] + self.current_exp  # current_exp 는 음수 이므로 +

        elif (self.current_exp <= 0) and (not self.is_level_min):  # 1레벨에서 경험치가 전부 사라지면
            self.current_exp = 0
            self.is_level_min = True
            pass

    def shoot(self):
        if len(self.bullets) < self.max_shoot_count:
            bullet = MissileBullet(self.x, self.y, self.shoot_dir, self.range, self.level)
            game_world.add_object(bullet, 1)

            self.bullets.append(bullet)


class Blade(Arms):
    arm_image = None

    def __init__(self):
        if Blade.arm_image is None:
            Blade.arm_image = load_image('./Image/Arms/Spur.png')

        self.level = 1
        self.MAX_BULLETS = INFINITE
        self.MAX_EXP = [20, 40, 60]
        self.damages = [15, 18, 30]  # 1레벨, 2레벨, 3레벨        거리에 따른 데미지 차이 있음
        self.current_exp = 0
        self.current_bullets = 0
        self.max_shoot_count = 1    # 최대 연사 수
        self.range = 200

        self.frame_x = 0
        self.frame_y = 0
        self.frame_size_x = 0
        self.frame_size_y = 0
        self.shoot_dir = RIGHT
        self.bullets = []

        self.is_level_max = False
        self.is_level_min = False

        self.x, self.y, self.move_dir = 400, 300, RIGHT
        pass

    def shoot(self):
        if len(self.bullets) < self.max_shoot_count:
            bullet = BladeAttack(self.x, self.y, self.shoot_dir, self.range, self.level)
            game_world.add_object(bullet, 1)

            self.bullets.append(bullet)

    def update(self):
        # 레벨 증가
        if self.is_level_min and self.current_exp > 0:  # 1레벨, 경험치 0이었는데 증가시
            self.is_level_min = False

        if (self.level is 3) and (not self.is_level_max):
            if self.current_exp >= self.MAX_EXP[self.level - 1]:
                self.current_exp = self.MAX_EXP[self.level - 1]
                self.is_level_max = True
            pass
        elif (self.level is 1) or (self.level is 2):
            if self.current_exp > self.MAX_EXP[self.level - 1]:
                self.current_exp -= self.MAX_EXP[self.level - 1]
                self.level += 1

        # 레벨 감소
        if self.is_level_max and (self.current_exp is not self.MAX_EXP[self.level - 1]):  # MAX 이고, 경험치가 MAX 는 아니면
            self.is_level_max = False

        elif self.level > 1:
            if self.current_exp < 0:  # 레벨 감소 발생
                self.level -= 1
                self.current_exp = self.MAX_EXP[self.level - 1] + self.current_exp  # current_exp 는 음수 이므로 +

        elif (self.current_exp <= 0) and (not self.is_level_min):  # 1레벨에서 경험치가 전부 사라지면
            self.current_exp = 0
            self.is_level_min = True
            pass
        pass

    def draw(self):  # 공격시만 무기가 보이므로 따로 그림
        pass


class Nemesis(Arms):
    arm_image = None

    def __init__(self):
        if Nemesis.arm_image is None:
            Nemesis.arm_image = load_image('./Image/Arms/Nemesis.png')      # 24 * 94

        self.level = 1
        self.MAX_BULLETS = 30
        self.MAX_EXP = [10, 5, 1]
        self.damages = [12, 8, 1]  # 1레벨, 2레벨, 3레벨
        self.current_exp = 0
        self.current_bullets = 0
        self.max_shoot_count = 2    # 최대 연사 수
        self.range = 500

        self.frame_x = 0
        self.frame_y = 0
        self.frame_size_x = 0
        self.frame_size_y = 0
        self.shoot_dir = RIGHT
        self.bullets = []

        self.is_level_max = False
        self.is_level_min = False

        self.x, self.y, self.move_dir = 400, 300, RIGHT
        pass

    def update(self):
        if self.shoot_dir is UP:
            self.frame_size_x = 5
            self.frame_size_y = 12

            if self.player_move_dir is LEFT:
                self.frame_x = 10
                self.frame_y = 56
            elif self.player_move_dir is RIGHT:
                self.frame_x = 9
                self.frame_y = 40

        elif self.shoot_dir is DOWN:
            self.frame_size_x = 5
            self.frame_size_y = 12

            if self.player_move_dir is LEFT:
                self.frame_x = 12
                self.frame_y = 21
            elif self.player_move_dir is RIGHT:
                self.frame_x = 7
                self.frame_y = 5

        elif self.shoot_dir is LEFT:        # y = 94
            self.frame_size_x = 12
            self.frame_size_y = 5
            self.frame_x = 3
            self.frame_y = 87

        elif self.shoot_dir is RIGHT:
            self.frame_size_x = 12
            self.frame_size_y = 5
            self.frame_x = 9
            self.frame_y = 71

        # 레벨 증가
        if self.is_level_min and self.current_exp > 0:  # 1레벨, 경험치 0이었는데 증가시
            self.is_level_min = False

        if (self.level is 3) and (not self.is_level_max):
            if self.current_exp >= self.MAX_EXP[self.level - 1]:
                self.current_exp = self.MAX_EXP[self.level - 1]
                self.is_level_max = True
            pass
        elif (self.level is 1) or (self.level is 2):
            if self.current_exp > self.MAX_EXP[self.level - 1]:
                self.current_exp -= self.MAX_EXP[self.level - 1]
                self.level += 1

        # 레벨 감소
        if self.is_level_max and (self.current_exp is not self.MAX_EXP[self.level - 1]):  # MAX 이고, 경험치가 MAX 는 아니면
            self.is_level_max = False

        elif self.level > 1:
            if self.current_exp < 0:  # 레벨 감소 발생
                self.level -= 1
                self.current_exp = self.MAX_EXP[self.level - 1] + self.current_exp  # current_exp 는 음수 이므로 +

        elif (self.current_exp <= 0) and (not self.is_level_min):  # 1레벨에서 경험치가 전부 사라지면
            self.current_exp = 0
            self.is_level_min = True
            pass

    def shoot(self):
        if len(self.bullets) < self.max_shoot_count:
            bullet = NemesisBullet(self.x, self.y, self.shoot_dir, self.range, self.level)
            game_world.add_object(bullet, 1)

            self.bullets.append(bullet)

