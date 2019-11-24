import random
import json
import os

from pico2d import *

import game_framework
import game_world


from player import Player
from tile import Tile
from missile_turret import MissileTurret
from arms import Spur, MissileLauncher, Blade, Nemesis


name = "MainState"

player = None
background = None
arms = []


def enter():
    global player, background
    player = Player()
    tile1 = Tile(200, 30)
    tile2 = Tile(600, 30)
    missile_turret1 = MissileTurret(100, 500)        # 임시 배치
    missile_turret2 = MissileTurret(600, 500)        # 임시 배치

    game_world.add_object(tile1, 0)
    game_world.add_object(tile2, 0)
    game_world.add_object(player, 1)
    game_world.add_object(missile_turret1, 1)
    game_world.add_object(missile_turret2, 1)
    background = load_image('./Image/Map/Cave.png')

    global arms
    arms = player.arms
    game_world.add_object(arms[player.current_arm], 1)


def exit():
    global background
    game_world.clear()
    del background


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            player.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    arms[player.current_arm].synchronize_to_player(*player.get_player_move())





def draw():
    clear_canvas()
    background.clip_draw(0, 12, 32, 40, 200, 150, 400, 300)     # 배경
    background.clip_draw(0, 12, 32, 40, 600, 150, 400, 300)     # 배경
    background.clip_draw(0, 12, 32, 40, 200, 450, 400, 300)     # 배경
    background.clip_draw(0, 12, 32, 40, 600, 450, 400, 300)     # 배경
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






