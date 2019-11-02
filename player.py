from pico2d import *

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SHIFT_DOWN, SHIFT_UP, DASH_TIMER, SPACE,\
    UP_UP, UP_DOWN, DOWN_UP, DOWN_DOWN = range(13)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
}


class IdleState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += 1
        elif event == LEFT_DOWN:
            player.velocity_x -= 1
        elif event == RIGHT_UP:
            player.velocity_x -= 1
        elif event == LEFT_UP:
            player.velocity_x += 1
        elif event == UP_DOWN:
            player.y_dir += 1
        elif event == UP_UP:
            player.y_dir -= 1
        elif event == DOWN_DOWN:
            player.y_dir -= 1
        elif event == DOWN_UP:
            player.y_dir += 1
        elif event == SPACE:
            if player.jump_count > 0:
                player.jump()
                player.jump_count -= 1
        player.timer = 1000
        player.frame = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.timer -= 1

        player.do_jump()
        player.y = clamp(90, player.y, 600 - 40)        # 현 바닥 아래, 맵 위로는 못나감

        if player.timer == 0:
            player.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(player):
        if player.y_dir > 0:       # 위를 바라봄
            if player.x_dir == 1:
                player.image.clip_draw((player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw((player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
        else:                      # 위를 바라보지않음
            if player.x_dir == 1:
                player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


class RunState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += 1
        elif event == LEFT_DOWN:
            player.velocity_x -= 1
        elif event == RIGHT_UP:
            player.velocity_x -= 1
        elif event == LEFT_UP:
            player.velocity_x += 1
        elif event == UP_DOWN:
            player.y_dir += 1
        elif event == UP_UP:
            player.y_dir -= 1
        elif event == DOWN_DOWN:
            player.y_dir -= 1
        elif event == DOWN_UP:
            player.y_dir += 1
        elif event == SPACE:
            if player.jump_count > 0:
                player.jump_count -= 1
                player.jump()
        player.x_dir = player.velocity_x

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 3
        player.timer -= 1
        player.x += player.velocity_x
        player.x = clamp(25, player.x, 800 - 25)

        player.do_jump()
        player.y = clamp(90, player.y, 600 - 40)
        pass

    @staticmethod
    def draw(player):
        if player.y_dir > 0:       # 위를 바라봄
            if player.velocity_x == 1:
                player.image.clip_draw((player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw((player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
        else:                      # 위를 바라보지않음
            if player.x_dir == 1:
                player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


class SleepState:
    @staticmethod
    def enter(player, event):
        player.frame = 0

    @staticmethod
    def exit(player, event):
        if event == SPACE:
            player.jump()
        pass

    @staticmethod
    def do(player):
        player.frame = 9

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


class DashState:    # 부스트 형식으로 해야함
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity_x += 1
        elif event == LEFT_DOWN:
            player.velocity_x -= 1
        elif event == RIGHT_UP:
            player.velocity_x -= 1
        elif event == LEFT_UP:
            player.velocity_x += 1
        elif event == UP_DOWN:
            player.y_dir += 1
        elif event == UP_UP:
            player.y_dir -= 1
        elif event == DOWN_DOWN:
            player.y_dir -= 1
        elif event == DOWN_UP:
            player.y_dir += 1
        player.x_dir = player.velocity_x
        player.timer = 100
        player.jump_timer = 0           # 점프 후 대쉬 시 점프했던 것 초기화

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.timer -= 1
        player.x += (player.velocity_x * 2)
        player.x = clamp(25, player.x, 800 - 25)

        if player.timer == 0:
            player.add_event(DASH_TIMER)

        player.y = clamp(90, player.y, 600 - 40)
        pass

    @staticmethod
    def draw(player):
        if player.velocity_x == 1:
            player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SLEEP_TIMER: SleepState, SHIFT_DOWN: IdleState,
                SHIFT_UP: IdleState, SPACE: IdleState,
                UP_UP: IdleState, UP_DOWN: IdleState,
                DOWN_UP: IdleState, DOWN_DOWN: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState,
               SPACE: RunState, UP_UP: RunState, UP_DOWN: RunState,
               DOWN_UP: RunState, DOWN_DOWN: RunState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                 LEFT_UP: RunState, RIGHT_UP: RunState,
                 SHIFT_DOWN: SleepState, SHIFT_UP: SleepState,
                 SPACE: IdleState, UP_UP: IdleState, UP_DOWN: IdleState,
                 DOWN_UP: IdleState, DOWN_DOWN: IdleState},
    DashState: {LEFT_UP: IdleState, RIGHT_UP: IdleState,
                LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                SHIFT_UP: RunState, SHIFT_DOWN: DashState,
                DASH_TIMER: RunState, SPACE: DashState,
                UP_UP: DashState, UP_DOWN: DashState,
                DOWN_UP: DashState, DOWN_DOWN: DashState}
}


class Player:
    def __init__(self):
        self.x, self.y = 500, 90
        self.image = load_image('character_sprite.png')      # 48*48 이 캐릭터 크기
        self.x_dir = 1
        self.y_dir = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.frame = 0          # 캐릭터 프레임
        self.timer = 0          # IDLE 상태에서 휴식 타이머, 대쉬 지속시간 타이머
        self.jump_timer = 0     # 점프 체공시간
        self.jump_count = 1     # 2단 점프
        self.dash_count = 1     # 공중에서 대쉬 횟수
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

    def jump(self):
        self.jump_timer = 200

    def do_jump(self):
        if self.jump_timer >= 100:
            self.jump_timer -= 1
            self.y += 1
        elif self.jump_timer > 0:
            self.jump_timer -= 1
            self.y -= 1
        elif self.jump_timer == 0:
            self.y -= 1
            if self.y == 90:              # 바닥의 위에 닿으면 점프 횟수 초기화
                self.jump_count = 1
