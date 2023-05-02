import pygame as pg
import copy
from random import randint


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

class Values():
    """Class that stores all the basic information"""
    block_on_screen = False
    
    class Sounds():
        pg.mixer.init(44100, -16,2,2048)
        TETRIS_MUSIC = pg.mixer.Sound('Tetris_theme.mp3')

    class Cooldown():
        PUSH_DOWN_COOLDOWN = 0.1
        PUSH_SIDE_COOLDOWN = 0.2
        ROTATE_COOLDOWN = 0.3

    class Game_properties():
        BLOCK_SIZE = 50
        WIDTH = BLOCK_SIZE * 10
        HEIGHT = BLOCK_SIZE * 20
        TICK_RATE = 30
        TITLE = 'Tetris by LSTEP'
        BACKGROUND_COLOR = Colors.BEIGE

class Timer():
    push_down = -1
    push_side = -1
    rotate = -1

    def count():
        if Timer.push_down != -1:
            Timer.push_down += 1
        if Timer.push_down / Values.Game_properties.TICK_RATE == Values.Cooldown.PUSH_DOWN_COOLDOWN:
            Timer.push_down = -1

        if Timer.push_side != -1:
            Timer.push_side += 1
        if Timer.push_side / Values.Game_properties.TICK_RATE == Values.Cooldown.PUSH_SIDE_COOLDOWN:
            Timer.push_side = -1
        
        if Timer.rotate != -1:
            Timer.rotate += 1
        if Timer.rotate / Values.Game_properties.TICK_RATE == Values.Cooldown.ROTATE_COOLDOWN:
            Timer.rotate = -1


class Block():
    moving_blocks = []
    static_blocks = []
  
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)

    def display(self):
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)
        pg.draw.rect(Game.WINDOW, self.color, self.object)

    def push_down(self):
        self.y += Values.Game_properties.BLOCK_SIZE
    
    def should_fall(self):
        if self.y + Values.Game_properties.BLOCK_SIZE == Values.Game_properties.HEIGHT:
            return True
        for block in Block.static_blocks:
            if self.y + Values.Game_properties.BLOCK_SIZE == block.y and self.x == block.x:
                return True
        return False

    def push_side(self, side):
        if side == 'left':
            self.x -= Values.Game_properties.BLOCK_SIZE
        else:
            self.x += Values.Game_properties.BLOCK_SIZE
    
    def rotate(self, side):
        pass
        

class Block_types():
      block_types = [
        [Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE, Colors.GOLD),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 2, Colors.GOLD),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 3, Colors.GOLD),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 4, Colors.GOLD)],
        
        [Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE, Colors.CYAN),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 2, Colors.CYAN),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 3, Colors.CYAN),
        Block(Values.Game_properties.BLOCK_SIZE * 5, -Values.Game_properties.BLOCK_SIZE * 3, Colors.CYAN)],

        [Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE, Colors.BLUE),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 2, Colors.BLUE),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 3, Colors.BLUE),
        Block(Values.Game_properties.BLOCK_SIZE * 3, -Values.Game_properties.BLOCK_SIZE * 3, Colors.BLUE)],

        [Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE, Colors.PURPLE),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 2, Colors.PURPLE),
        Block(Values.Game_properties.BLOCK_SIZE * 3, -Values.Game_properties.BLOCK_SIZE * 2, Colors.PURPLE),
        Block(Values.Game_properties.BLOCK_SIZE * 5, -Values.Game_properties.BLOCK_SIZE * 2, Colors.PURPLE)],

        [Block(Values.Game_properties.BLOCK_SIZE * 3, -Values.Game_properties.BLOCK_SIZE * 2, Colors.GREEN),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 2, Colors.GREEN),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 1, Colors.GREEN),
        Block(Values.Game_properties.BLOCK_SIZE * 5, -Values.Game_properties.BLOCK_SIZE * 1, Colors.GREEN)],

        [Block(Values.Game_properties.BLOCK_SIZE * 3, -Values.Game_properties.BLOCK_SIZE * 1, Colors.RED),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 1, Colors.RED),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 2, Colors.RED),
        Block(Values.Game_properties.BLOCK_SIZE * 5, -Values.Game_properties.BLOCK_SIZE * 2, Colors.RED)],

        [Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 1, Colors.YELLOW),
        Block(Values.Game_properties.BLOCK_SIZE * 4, -Values.Game_properties.BLOCK_SIZE * 2, Colors.YELLOW),
        Block(Values.Game_properties.BLOCK_SIZE * 5, -Values.Game_properties.BLOCK_SIZE * 1, Colors.YELLOW),
        Block(Values.Game_properties.BLOCK_SIZE * 5, -Values.Game_properties.BLOCK_SIZE * 2, Colors.YELLOW)]
      ]


class Game():
    WINDOW = pg.display.set_mode((Values.Game_properties.WIDTH, Values.Game_properties.HEIGHT))
    pg.display.set_caption(Values.Game_properties.TITLE)

    def __init__(self):
        pg.init()
        Values.Sounds.TETRIS_MUSIC.set_volume(0.1)
        Values.Sounds.TETRIS_MUSIC.play(-1)
        self.clock = pg.time.Clock()
        self.run = True
        Game.add_new_blocks()
        while self.run == True:
            self.clock.tick(Values.Game_properties.TICK_RATE)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
            
            if Timer.push_down == -1:
                Game.push_down()
                Timer.push_down += 1
            
            Game.controls()
            Game.remove_blocks()
            Game.remove_row()
            Game.visuals()
            Timer.count()
            

    def visuals():
        Game.WINDOW.fill(Values.Game_properties.BACKGROUND_COLOR)
        for block in Block.moving_blocks:
            block.display()
        for block in Block.static_blocks:
            block.display()

        pg.display.update()

    def push_down():
        for block in Block.moving_blocks:
            block.push_down()

    def add_new_blocks():
        Block.moving_blocks = copy.deepcopy(Block_types.block_types[randint(0, 0)])#len(Block_types.block_types)-1

    def controls():
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_a] and Timer.push_side == -1:
            for block in Block.moving_blocks:
                block.push_side("left")
            Timer.push_side = 0
        if keys_pressed[pg.K_d] and Timer.push_side == -1:
            for block in Block.moving_blocks:
                block.push_side("right")
            Timer.push_side = 0

        if keys_pressed[pg.K_w] and Timer.rotate == -1:
            for block in Block.moving_blocks:
                block.rotate("left")
            Timer.rotate = 0
        if keys_pressed[pg.K_s] and Timer.rotate == -1:
            for block in Block.moving_blocks:
                block.rotate("right")
            Timer.rotate = 0

    def remove_blocks():
        for block in Block.moving_blocks:
            if block.should_fall():
                Block.static_blocks += Block.moving_blocks 
                Block.moving_blocks = []
                Game.add_new_blocks()
                break

    def remove_row():
        y_values = [Values.Game_properties.BLOCK_SIZE * value for value in range(20)]
        blocks_to_remove = []
        
        for y_value in y_values:
            num_of_blocks = 0
            
            for block in Block.static_blocks:
                if block.y == y_value:
                    num_of_blocks += 1
                    
            if num_of_blocks == 10:
                for block in Block.static_blocks:
                    if block.y == y_value:
                        blocks_to_remove.append(block)

        for block in blocks_to_remove:
            Block.static_blocks.remove(block)
            


if __name__ == "__main__":
    Game()
