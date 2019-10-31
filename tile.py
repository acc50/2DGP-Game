from pico2d import *


class Tile:
    def __init__(self, x, y):
        self.image = load_image('tile.png')
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 300, 40)
