from pico2d import *

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, UP_UP, UP_DOWN, \
DOWN_UP, DOWN_DOWN, SLEEP_TIMER, SHIFT_DOWN, SHIFT_UP, DASH_TIMER = range(12)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP
}


class IdleState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity += 1
        elif event == LEFT_DOWN:
            player.velocity -= 1
        elif event == RIGHT_UP:
            player.velocity -= 1
        elif event == LEFT_UP:
            player.velocity += 1
        player.timer = 1000

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.timer -= 1
        if player.timer == 0:
            player.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image.clip_draw(player.frame * 100, 300, 100, 100, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 100, 200, 100, 100, player.x, player.y)


class RunState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity += 1
            player.dash_direction = 1
        elif event == LEFT_DOWN:
            player.velocity -= 1
            player.dash_direction = 5
        elif event == RIGHT_UP:
            player.velocity -= 1
            player.dash_direction = 0
        elif event == LEFT_UP:
            player.velocity += 1
            player.dash_direction = 0
        player.x_dir = player.velocity

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.timer -= 1
        player.x += player.velocity
        player.x = clamp(25, player.x, 800 - 25)
        pass

    @staticmethod
    def draw(player):
        if player.velocity == 1:
            player.image.clip_draw(player.frame * 100, 100, 100, 100, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 100, 0, 100, 100, player.x, player.y)


class RunState2:
    @staticmethod
    def enter(player, event):
        if player.x_dir > 0 & event == DOWN_DOWN:
            player.dash_direction = 1

        elif event == LEFT_DOWN:
            player.velocity -= 1
        elif event == RIGHT_UP:
            player.velocity -= 1
        elif event == LEFT_UP:
            player.velocity += 1
        player.x_dir = player.velocity

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.timer -= 1
        player.x += player.velocity
        player.x = clamp(25, player.x, 800 - 25)
        pass

    @staticmethod
    def draw(player):
        if player.velocity == 1:
            player.image.clip_draw(player.frame * 100, 100, 100, 100, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 100, 0, 100, 100, player.x, player.y)


class SleepState:
    @staticmethod
    def enter(player, event):
        player.frame = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image.clip_composite_draw(player.frame * 100, 300, 100, 100,
                                             3.141592 / 2, '', player.x - 25, player.y - 25, 100, 100)
        else:
            player.image.clip_composite_draw(player.frame * 100, 200, 100, 100,
                                             -3.141592 / 2, '', player.x + 25, player.y - 25, 100, 100)


class DashState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity += 1
        elif event == LEFT_DOWN:
            player.velocity -= 1
        elif event == RIGHT_UP:
            player.velocity -= 1
        elif event == LEFT_UP:
            player.velocity += 1
        player.x_dir = player.velocity
        player.dash_timer = 100

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.timer -= 1
        player.dash_timer -= 1
        player.x += (player.velocity * 3)
        player.x = clamp(25, player.x, 800 - 25)
        if player.dash_timer == 0:
            player.add_event(DASH_TIMER)

    @staticmethod
    def draw(player):
        if player.velocity == 1:
            player.image.clip_draw(player.frame * 100, 100, 100, 100, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 100, 0, 100, 100, player.x, player.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                UP_UP: IdleState, DOWN_UP: IdleState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                UP_DOWN: IdleState, DOWN_DOWN: IdleState,
                SLEEP_TIMER: SleepState, SHIFT_DOWN: IdleState,
                SHIFT_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               UP_UP: IdleState, DOWN_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               UP_DOWN: RunState2, DOWN_DOWN: RunState2,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState},
    RunState2: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                UP_UP: IdleState, DOWN_UP: IdleState,
                LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                UP_DOWN: IdleState, DOWN_DOWN: IdleState,
                SHIFT_DOWN: DashState, SHIFT_UP: RunState2},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                 UP_DOWN: SleepState, DOWN_DOWN: SleepState,
                 LEFT_UP: RunState, RIGHT_UP: RunState,
                 UP_UP: SleepState, DOWN_UP: SleepState,
                 SHIFT_DOWN: SleepState, SHIFT_UP: SleepState},
    DashState: {LEFT_UP: IdleState, RIGHT_UP: IdleState,
                UP_UP: IdleState, DOWN_UP: IdleState,
                LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                UP_DOWN: IdleState, DOWN_DOWN: IdleState,
                SHIFT_UP: RunState, SHIFT_DOWN: DashState,
                DASH_TIMER: RunState}
}


class Player:
    def __init__(self):
        self.x, self.y = 800 // 2, 90
        self.image = load_image('animation_sheet.png')
        self.x_dir = 1
        self.y_dir = 0
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.dash_timer = 0
        self.dash_direction = 0     # 3시 기준 시계방향으로 1~8
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
