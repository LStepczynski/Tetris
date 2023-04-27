import pygame as pg

class Base_Values:
    BLOCK_SIZE = 50
    WIDTH = BLOCK_SIZE * 10
    HEIGHT = BLOCK_SIZE * 20

    TITLE = 'Tetris by LSTEP'

class Game():
    def __init__(self):
        pg.init()

        self.WINDOW = pg.display.set_mode((Base_Values.WIDTH, Base_Values.HEIGHT))
        pg.display.set_caption(Base_Values.TITLE)

        self.clock = pg.time.Clock()
        self.run = True
        while self.run == True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False


if __name__ == "__main__":
    Game()
        