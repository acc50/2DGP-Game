import random
import json
import os

from pico2d import *

import game_framework


from player import Player
from grass import Grass



name = "MainState"

player = None
grass = None
font = None



def enter():
    global player, grass
    player = Player()
    grass = Grass()


def exit():
    global player, grass
    del player
    del grass



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
    player.update()

def draw():
    clear_canvas()
    grass.draw()
    player.draw()
    update_canvas()






