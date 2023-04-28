import pygame as pg

class Values():
    """Class that stores all the basic information"""
    class Cooldown():
        PUSH_DOWN_COOLDOWN = 0.5
    
    class Game_properties():
        BLOCK_SIZE = 50
        WIDTH = BLOCK_SIZE * 10
        HEIGHT = BLOCK_SIZE * 20
        TICK_RATE = 30
        TITLE = 'Tetris by LSTEP'
    
    class Colors():
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        YELLOW = (255, 255, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        MAGENTA = (255, 0, 255)
        CYAN = (0, 255, 255)
        GRAY = (128, 128, 128)
        ORANGE = (255, 165, 0)
        PURPLE = (128, 0, 128)
        BROWN = (165, 42, 42)
        PINK = (255, 192, 203)
        GOLD = (255, 215, 0)
        SILVER = (192, 192, 192)
        BEIGE = (245, 245, 220)


class Timer():
    push_down = -1
    def count():
        if Timer.push_down != -1:
            Timer.push_down += 1
        
        if Timer.push_down / Values.Game_properties.TICK_RATE == Values.Cooldown.PUSH_DOWN_COOLDOWN:
            Timer.push_down = -1


class Block():
    blocks = []

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)

    def display(self):
        Game.WINDOW.fill(Values.Colors.BLACK)
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)
        pg.draw.rect(Game.WINDOW, self.color, self.object)

        pg.display.update()
    
    def push_down(self):
        if Timer.push_down == -1:
            self.y += Values.Game_properties.BLOCK_SIZE
            Timer.push_down = 0
            
    
class Game():
    WINDOW = pg.display.set_mode((Values.Game_properties.WIDTH, Values.Game_properties.HEIGHT))
    pg.display.set_caption(Values.Game_properties.TITLE)

    def __init__(self):
        pg.init()
        Block.blocks.append(Block(0, 0, Values.Colors.GOLD))
        self.clock = pg.time.Clock()
        self.run = True
        
        while self.run == True:
            self.clock.tick(Values.Game_properties.TICK_RATE)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
            
            Game.push_down()
            Game.visuals()
            Timer.count()

        
    def visuals():
        for block in Block.blocks:
            block.display()
    
    def push_down():
        for block in Block.blocks:
            block.push_down()
        


if __name__ == "__main__":
    Game()
        