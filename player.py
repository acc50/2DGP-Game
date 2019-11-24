from pico2d import *

from boost import Boost
import game_world
import game_framework
from arms import Spur, MissileLauncher, Blade, Nemesis


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # 14 Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

BOOST_SPEED_KMPH = 50.0
BOOST_SPEED_MPM = (BOOST_SPEED_KMPH * 1000.0 / 60.0)
BOOST_SPEED_MPS = (BOOST_SPEED_MPM / 60.0)
BOOST_SPEED_PPS = (BOOST_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

FALL_SPEED = 300
JUMP_SPEED = 300
MAX_BOOST_GAUGE = 1000

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, BOOST_TIMER, SPACE_DOWN, \
 SPACE_UP, UP_UP, UP_DOWN, DOWN_UP, DOWN_DOWN, BOOST, X_DOWN, X_UP, \
    A_DOWN, S_DOWN = range(17)

UP, DOWN, LEFT, RIGHT = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYDOWN, SDLK_x): X_DOWN,
    (SDL_KEYUP, SDLK_x): X_UP,
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYDOWN, SDLK_s): S_DOWN
}


class IdleState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity_x += RUN_SPEED_PPS

        elif event == X_DOWN:
            print('hello')
        elif event == X_UP:
            pass
        elif event == A_DOWN:           # 무기 교체 -> 현재 무기 월드에서 삭제, 다음무기 월드에서 생성
            game_world.remove_object(player.arms[player.current_arm])

            player.current_arm -= 1
            if player.current_arm < 0:
                player.current_arm = 3

            game_world.add_object(player.arms[player.current_arm], 1)

        elif event == S_DOWN:
            game_world.remove_object(player.arms[player.current_arm])
            player.current_arm = (player.current_arm + 1) % 4
            game_world.add_object(player.arms[player.current_arm], 1)

        if event == UP_DOWN:
            player.view_dir_y += 1
        elif event == UP_UP:
            player.view_dir_y -= 1
        elif event == DOWN_DOWN:
            player.view_dir_y -= 1
        elif event == DOWN_UP:
            player.view_dir_y += 1

        if event == SPACE_DOWN:
            if player.is_jump is False:
                player.is_jump = True
            elif player.is_jump:  # 점프를 한 상태에선 부스트 사용함
                player.boost_gauge = MAX_BOOST_GAUGE
                player.is_boost = True
                player.boost_frame = 0

                player.set_boost_dir()

                player.add_event(BOOST)
        elif event == SPACE_UP:
            player.jump_timer = 200
        player.timer = 1000
        player.frame = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.timer -= 1

        if player.is_jump and (player.jump_timer < 200):
            player.y += 1
            player.jump_timer += 1
        else:
            player.y -= 1
            if player.y <= 90:
                player.is_jump = False
                player.jump_timer = 0

        player.y = clamp(90, player.y, 600 - 40)  # 현 바닥 아래, 맵 위로는 못나감

        if player.timer == 0:
            player.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(player):
        if player.view_dir_y > 0:  # 위를 바라봄
            if player.dir_x > 0:
                player.image.clip_draw(int(player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(int(player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
        else:  # 위를 바라보지않음
            if player.dir_x > 0:
                player.image.clip_draw(int(player.frame) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(int(player.frame) * 48, 240, 48, 48, player.x, player.y)


class RunState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity_x -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity_x += RUN_SPEED_PPS

        elif event == X_DOWN:
            pass
        elif event == X_UP:
            pass
        elif event == A_DOWN:
            player.current_arm = -1
            if player.current_arm < 0:
                player.current_arm = 3
        elif event == S_DOWN:
            player.current_arm = (player.current_arm + 1) % 4

        player.dir_x = clamp(-1, player.velocity_x, 1)

        if event == UP_DOWN:
            player.view_dir_y += 1
        elif event == UP_UP:
            player.view_dir_y -= 1
        elif event == DOWN_DOWN:
            player.view_dir_y -= 1
        elif event == DOWN_UP:
            player.view_dir_y += 1

        if event == SPACE_DOWN:
            if player.is_jump is False:
                player.is_jump = True
            elif player.is_jump:  # 점프를 한 상태에선 부스트 사용함
                player.boost_gauge = MAX_BOOST_GAUGE
                player.is_boost = True
                player.boost_frame = 0

                player.set_boost_dir()

                player.add_event(BOOST)
        elif event == SPACE_UP:
            player.jump_timer = 200

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.velocity_x * game_framework.frame_time
        player.x = clamp(25, player.x, 800 - 25)

        if player.is_jump and (player.jump_timer < 200):
            player.y += 1
            player.jump_timer += 1
        else:
            player.y -= 1
            if player.y == 90:
                player.is_jump = False
                player.jump_timer = 0

        player.y = clamp(90, player.y, 600 - 40)
        pass

    @staticmethod
    def draw(player):
        if player.view_dir_y > 0:  # 위를 바라봄
            if player.velocity_x > 0:
                player.image.clip_draw(int(player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(int(player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
        else:  # 위를 바라보지않음
            if player.velocity_x > 0:
                player.image.clip_draw(int(player.frame) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(int(player.frame) * 48, 240, 48, 48, player.x, player.y)


class SleepState:
    @staticmethod
    def enter(player, event):

        if event == X_UP:
            pass
        elif event == X_DOWN:
            pass
        elif event == A_DOWN:
            player.current_arm = -1
            if player.current_arm < 0:
                player.current_arm = 3
        elif event == S_DOWN:
            player.current_arm = (player.current_arm + 1) % 4

        player.frame = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = 9

    @staticmethod
    def draw(player):
        if player.dir_x > 0:
            player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


class BoostState:  # 부스트 형식으로 해야함
    @staticmethod
    def enter(player, event):
        if player.boost_dir is UP or player.boost_dir is DOWN:      # 위 or 아래쪽 부스트시엔 좌우이동 X
            if event == RIGHT_DOWN:
                player.view_dir_x += 1
            elif event == LEFT_DOWN:
                player.view_dir_x -= 1
            elif event == RIGHT_UP:
                player.view_dir_x -= 1
            elif event == LEFT_UP:
                player.view_dir_x += 1

            elif event == X_UP:
                pass
            elif event == X_DOWN:
                print('attack')
                pass
            elif event == A_DOWN:
                player.current_arm = -1
                if player.current_arm < 0:
                    player.current_arm = 3
            elif event == S_DOWN:
                player.current_arm = (player.current_arm + 1) % 4

            if event == UP_DOWN:
                player.view_dir_y += 1
            elif event == UP_UP:
                player.view_dir_y -= 1
            elif event == DOWN_DOWN:
                player.view_dir_y -= 1
            elif event == DOWN_UP:
                player.view_dir_y += 1

            if player.boost_dir is UP:
                player.velocity_y = BOOST_SPEED_PPS
            else:
                player.velocity_y = -BOOST_SPEED_PPS

        elif player.boost_dir is LEFT or player.boost_dir is RIGHT:  # 왼쪽 or 오른쪽 부스트시엔 좌우이동 O
            player.velocity_x = player.dir_x * BOOST_SPEED_PPS

            if event == RIGHT_DOWN:
                player.velocity_x += BOOST_SPEED_PPS
            elif event == LEFT_DOWN:
                player.velocity_x -= BOOST_SPEED_PPS
            elif event == RIGHT_UP:
                player.velocity_x -= BOOST_SPEED_PPS
            elif event == LEFT_UP:
                player.velocity_x += BOOST_SPEED_PPS

            if event == UP_DOWN:
                player.view_dir_y += 1
            elif event == DOWN_DOWN:
                player.view_dir_y -= 1
            elif event == UP_UP:
                player.view_dir_y -= 1
            elif event == DOWN_UP:
                player.view_dir_y += 1
            pass

        # player.dir_x = clamp(-1, player.velocity_x, 1)

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.boost_gauge -= 1

        if player.velocity_y is not 0:
            player.y += player.velocity_y * game_framework.frame_time
            # 바닥과 충돌 시 처리 필요
        else:
            player.x += player.velocity_x * game_framework.frame_time

        if player.boost_gauge == 0:
            player.is_boost = True
            player.add_event(BOOST_TIMER)
            # player.dir_x = 0

        player.x = clamp(25, player.x, 800 - 25)
        player.y = clamp(90, player.y, 600 - 40)
        pass

    @staticmethod
    def draw(player):
        if player.view_dir_y > 0:  # 위를 바라봄
            if player.velocity_x > 0:
                player.image.clip_draw(int(player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
                boost = Boost(player.x, player.y - 35, 0, -10)
                game_world.add_object(boost, 1)
            else:
                player.image.clip_draw(int(player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
                boost = Boost(player.x, player.y - 35, 0, -10)
                game_world.add_object(boost, 1)
        elif player.view_dir_y < 0:  # 아래를 바라봄
            if player.velocity_x > 0:
                player.image.clip_draw(6 * 48, 192, 48, 48, player.x, player.y)
                boost = Boost(player.x, player.y + 35, 0, +10)
                game_world.add_object(boost, 1)
            else:
                player.image.clip_draw(6 * 48, 240, 48, 48, player.x, player.y)
                boost = Boost(player.x, player.y + 35, 0, +10)
                game_world.add_object(boost, 1)
        else:  # 아래 또는 위를 바라보고 있지 않음
            if player.velocity_x > 0:
                player.image.clip_draw(int(player.frame) * 48, 192, 48, 48, player.x, player.y)
                boost = Boost(player.x - 35, player.y, -10, 0)
                game_world.add_object(boost, 1)
            else:
                player.image.clip_draw(int(player.frame) * 48, 240, 48, 48, player.x, player.y)
                boost = Boost(player.x + 35, player.y, 10, 0)
                game_world.add_object(boost, 1)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SLEEP_TIMER: SleepState, SPACE_DOWN: IdleState,
                SPACE_UP: IdleState, UP_UP: IdleState, UP_DOWN: IdleState,
                DOWN_UP: IdleState, DOWN_DOWN: IdleState, BOOST: BoostState,
                A_DOWN: IdleState, S_DOWN: IdleState, X_DOWN: IdleState, X_UP:IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SPACE_UP: RunState, SPACE_DOWN: RunState,
               UP_UP: RunState, UP_DOWN: RunState,
               DOWN_UP: RunState, DOWN_DOWN: RunState, BOOST: BoostState,
               A_DOWN: RunState, S_DOWN: RunState, X_DOWN: RunState, X_UP: RunState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                 LEFT_UP: RunState, RIGHT_UP: RunState,
                 SPACE_DOWN: IdleState, UP_UP: IdleState, UP_DOWN: IdleState,
                 DOWN_UP: IdleState, DOWN_DOWN: IdleState,
                 A_DOWN: SleepState, S_DOWN: SleepState, X_DOWN: SleepState, X_UP: SleepState},
    BoostState: {LEFT_UP: BoostState, RIGHT_UP: BoostState,
                 LEFT_DOWN: BoostState, RIGHT_DOWN: BoostState,
                 BOOST_TIMER: IdleState, SPACE_DOWN: BoostState,
                 SPACE_UP: IdleState, UP_UP: BoostState, UP_DOWN: BoostState,
                 DOWN_UP: BoostState, DOWN_DOWN: BoostState, A_DOWN: BoostState,
                 S_DOWN: BoostState, X_DOWN: BoostState, X_UP: BoostState}
}


class Player:
    def __init__(self):
        self.x, self.y = 500, 90
        self.image = load_image('./Image/Character/character_sprite.png')  # 48*48 이 캐릭터 크기
        self.dir_x = 1
        self.dir_y = 0

        self.move_dir = 0
        self.view_dir_x = 0
        self.view_dir_y = 0
        self.boost_dir = 0

        self.velocity_x = 0
        self.velocity_y = 0
        self.frame = 0  # 캐릭터 프레임
        self.timer = 0  # IDLE 상태에서 휴식 타이머, 대쉬 지속시간 타이머
        self.jump_timer = 0  # 점프 체공시간
        self.jump_count = 1  # 2단 점프
        self.is_jump = False
        self.is_boost = False
        self.boost_gauge = 1000

        self.arms = [Spur(), MissileLauncher(), Blade(), Nemesis()]
        self.current_arm = 0

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        pass

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def change_state(self, state):
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def set_boost_dir(self):
        if self.view_dir_y > 0:     # 위를 바라보고있으면
            self.boost_dir = UP
            pass
        else:
            if self.dir_x > 0:
                self.boost_dir = RIGHT
            elif self.dir_x < 0:
                self.boost_dir = LEFT
            elif self.view_dir_y < 0:
                self.boost_dir = DOWN
            elif self.dir_x == 0:
                self.boost_dir = UP
            pass

    def get_player_move(self):
        return self.velocity_x, self.move_dir, self.view_dir_x

