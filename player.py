from pico2d import *

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, BOOST_TIMER, SPACE_DOWN, \
 SPACE_UP, UP_UP, UP_DOWN, DOWN_UP, DOWN_DOWN, BOOST = range(13)

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
            player.dir_y += 1
        elif event == UP_UP:
            player.dir_y -= 1
        elif event == DOWN_DOWN:
            player.dir_y -= 1
        elif event == DOWN_UP:
            player.dir_y += 1
        elif event == SPACE_DOWN:
            if player.is_jump is False:
                player.is_jump = True
            elif player.is_jump:  # 점프를 한 상태에선 부스트 사용함
                player.boost_gauge = 1000
                player.velocity_y = player.dir_y
                print(player.velocity_y)
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
        if player.dir_y > 0:  # 위를 바라봄
            if player.dir_x == 1:
                player.image.clip_draw((player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw((player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
        else:  # 위를 바라보지않음
            if player.dir_x == 1:
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
            player.dir_y += 1
        elif event == UP_UP:
            player.dir_y -= 1
        elif event == DOWN_DOWN:
            player.dir_y -= 1
        elif event == DOWN_UP:
            player.dir_y += 1
        elif event == SPACE_DOWN:
            if player.is_jump is False:
                player.is_jump = True
            elif player.is_jump:  # 점프를 한 상태에선 부스트 사용함
                player.boost_gauge = 1000
                player.velocity_y = player.dir_y
                player.add_event(BOOST)
        elif event == SPACE_UP:
            player.jump_timer = 200
        player.dir_x = player.velocity_x

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 3
        player.timer -= 1
        player.x += player.velocity_x
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
        if player.dir_y > 0:  # 위를 바라봄
            if player.velocity_x == 1:
                player.image.clip_draw((player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw((player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
        else:  # 위를 바라보지않음
            if player.velocity_x == 1:
                player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


class SleepState:
    @staticmethod
    def enter(player, event):
        player.frame = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = 9

    @staticmethod
    def draw(player):
        if player.dir_x == 1:
            player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


class BoostState:  # 부스트 형식으로 해야함
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
            player.dir_y += 1
        elif event == UP_UP:
            player.dir_y -= 1
        elif event == DOWN_DOWN:
            player.dir_y -= 1
        elif event == DOWN_UP:
            player.dir_y += 1
        player.dir_x = player.velocity_x

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.boost_gauge -= 1

        if player.velocity_y == 1:
            player.y += (player.velocity_y * 1.3)
        elif player.velocity_y == -1:
            player.y += (player.velocity_y * 1.3)
            if player.y == 90:      # 바닥과 닿으면
                player.add_event(SPACE_UP)
        else:
            player.x += (player.velocity_x * 1.3)

        if player.boost_gauge == 0:
            player.add_event(BOOST_TIMER)
            player.dir_x = 0

        player.x = clamp(25, player.x, 800 - 25)
        player.y = clamp(90, player.y, 600 - 40)
        pass

    @staticmethod
    def draw(player):
        if player.dir_y > 0:  # 위를 바라봄
            if player.velocity_x == 1:
                player.image.clip_draw((player.frame + 3) * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw((player.frame + 3) * 48, 240, 48, 48, player.x, player.y)
        else:  # 위를 바라보지않음
            if player.velocity_x == 1:
                player.image.clip_draw(player.frame * 48, 192, 48, 48, player.x, player.y)
            else:
                player.image.clip_draw(player.frame * 48, 240, 48, 48, player.x, player.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SLEEP_TIMER: SleepState, SPACE_DOWN: IdleState,
                SPACE_UP: IdleState, UP_UP: IdleState, UP_DOWN: IdleState,
                DOWN_UP: IdleState, DOWN_DOWN: IdleState, BOOST: BoostState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SPACE_UP: RunState, SPACE_DOWN: RunState,
               UP_UP: RunState, UP_DOWN: RunState,
               DOWN_UP: RunState, DOWN_DOWN: RunState, BOOST: BoostState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                 LEFT_UP: RunState, RIGHT_UP: RunState,
                 SPACE_DOWN: IdleState, UP_UP: IdleState, UP_DOWN: IdleState,
                 DOWN_UP: IdleState, DOWN_DOWN: IdleState},
    BoostState: {LEFT_UP: BoostState, RIGHT_UP: BoostState,
                 LEFT_DOWN: BoostState, RIGHT_DOWN: BoostState,
                 BOOST_TIMER: RunState, SPACE_DOWN: BoostState,
                 SPACE_UP: IdleState, UP_UP: BoostState, UP_DOWN: BoostState,
                 DOWN_UP: BoostState, DOWN_DOWN: BoostState}
}


class Player:
    def __init__(self):
        self.x, self.y = 500, 90
        self.image = load_image('character_sprite.png')  # 48*48 이 캐릭터 크기
        self.dir_x = 1
        self.dir_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.frame = 0  # 캐릭터 프레임
        self.timer = 0  # IDLE 상태에서 휴식 타이머, 대쉬 지속시간 타이머
        self.jump_timer = 0  # 점프 체공시간
        self.jump_count = 1  # 2단 점프
        self.is_jump = False
        self.boost_gauge = 1000
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
