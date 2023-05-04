import pygame as pg
import copy
import random
import time


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
        PUSH_DOWN_COOLDOWN = 0.5
        PUSH_SIDE_COOLDOWN = 0.1
        ROTATE_COOLDOWN = 0.3

    class Game_properties():
        BLOCK_SIZE = 60
        WIDTH = BLOCK_SIZE * 18
        HEIGHT = BLOCK_SIZE * 20
        TICK_RATE = 30
        TITLE = 'Tetris by LSTEP'
        BACKGROUND_COLOR = Colors.BEIGE
        score = 0

class Fonts():
    b_size = Values.Game_properties.BLOCK_SIZE
    pg.font.init()
    SCORE = pg.font.SysFont('Tetris', Values.Game_properties.BLOCK_SIZE)
    
    TITLE_SCORE = SCORE.render("SCORE", 1, Colors.WHITE)
    score = SCORE.render(str(Values.Game_properties.score), 1, Colors.WHITE)
    HOLD = SCORE.render('HOLD', 1, Colors.WHITE)
    NEXT = SCORE.render('NEXT', 1, Colors.WHITE)

    texts = [(TITLE_SCORE, (b_size/6,b_size)), [score, (b_size/6, b_size*2)]]

    def update_score():
        score = Fonts.SCORE.render(str(Values.Game_properties.score), 1, Colors.WHITE)
        Fonts.texts[1][0] = score

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
  
    def __init__(self, x, y, color, index):
        self.x = x
        self.y = y
        self.color = color
        self.index = index
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
    

        

class Block_types():
      block_types = [
        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.CYAN, index) for pos_x, pos_y, index in zip([8 for _ in range(4)], [value+1 for value in range(4)], [value+1 for value in range(4)])],
        
        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.BLUE, index) for pos_x, pos_y, index in zip([8, 8, 8, 9], [1, 2, 3, 3], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.ORANGE, index) for pos_x, pos_y, index in zip([8, 8, 8, 7], [1, 2, 3, 3], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.PURPLE, index) for pos_x, pos_y, index in zip([8, 8, 7, 9], [1, 2, 2, 2], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.RED, index) for pos_x, pos_y, index in zip([7, 8, 8, 9], [2, 2, 1, 1], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.GREEN, index) for pos_x, pos_y, index in zip([7, 8, 8, 9], [1, 1, 2, 2], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.YELLOW, index) for pos_x, pos_y, index in zip([8, 8, 9, 9], [1, 2, 1, 2], [value+1 for value in range(4)])]
      ]

class Gui():
    left_square = pg.Rect(0,0, Values.Game_properties.BLOCK_SIZE*4, Values.Game_properties.HEIGHT)
    right_square = pg.Rect(Values.Game_properties.BLOCK_SIZE * 14 , 0, Values.Game_properties.BLOCK_SIZE*4, Values.Game_properties.HEIGHT)


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
                Values.Game_properties.score += 5
                Fonts.update_score()
                Timer.push_down += 1

            
            Game.controls()
            Game.remove_blocks()
            Game.remove_row()
            Game.visuals()
            Timer.count()
            

    def visuals():
        Game.WINDOW.fill(Values.Game_properties.BACKGROUND_COLOR)
      
        pg.draw.rect(Game.WINDOW, Colors.BLACK, Gui.left_square)
        pg.draw.rect(Game.WINDOW, Colors.BLACK, Gui.right_square)

        for text, coordinates in Fonts.texts:
            Game.WINDOW.blit(text, coordinates)

        for block in Block.moving_blocks:
            block.display()
        for block in Block.static_blocks:
            block.display()

        pg.display.update()

    def push_down():
        for block in Block.moving_blocks:
            block.push_down()

    def add_new_blocks():
        random.seed(time.time())
        Block.moving_blocks = copy.deepcopy(Block_types.block_types[random.randint(0, len(Block_types.block_types)-1)])
        Values.Game_properties.ROTATE_STAGE = 1

    def controls():
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_a] and Timer.push_side == -1:
            for block in Block.moving_blocks:
                if block.x - Values.Game_properties.BLOCK_SIZE < Values.Game_properties.BLOCK_SIZE * 4:
                    break
                block.push_side("left")
            Timer.push_side = 0
        if keys_pressed[pg.K_d] and Timer.push_side == -1:
            for block in reversed(Block.moving_blocks):
                if block.x + Values.Game_properties.BLOCK_SIZE > Values.Game_properties.BLOCK_SIZE * 13:
                    break    
                block.push_side("right")
            Timer.push_side = 0
        if keys_pressed[pg.K_s] and Timer.push_down != -1:
            Timer.push_down = -1
            Values.Game_properties.score += 5

        if keys_pressed[pg.K_w] and Timer.rotate == -1:
            Game.rotate()
            Timer.rotate = 0

    def remove_blocks():
        for block in Block.moving_blocks:
            if block.should_fall():
                Block.static_blocks += Block.moving_blocks 
                Block.moving_blocks = []
                Game.add_new_blocks()
                break

    def remove_row():
        y_values = list(reversed([Values.Game_properties.BLOCK_SIZE * value for value in range(20)]))

        for y_value in y_values:
            blocks_to_remove = []
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

            if blocks_to_remove:
                for block in Block.static_blocks:
                    if block.y < y_value:
                        block.y += Values.Game_properties.BLOCK_SIZE

    def rotate():
        if Block.moving_blocks[0].color != Colors.YELLOW:
            # Define the coordinates of the block
            blocks = []
            for block in Block.moving_blocks:
                blocks.append((block.x, block.y))

            # Define the center of rotation
            center = blocks[1]

            # Translate the block to the origin
            translated_block = [(x - center[0], y - center[1]) for x, y in blocks]

            # Rotate the block around the origin
            rotated_blocks = [(-y, x) for x, y in translated_block]

            # Translate the block back to its original position
            final_block = [(x + center[0], y + center[1]) for x, y in rotated_blocks]

            for block, index in zip(final_block, range(4)):
                Block.moving_blocks[index].x = block[0]
                Block.moving_blocks[index].y = block[1]

    

if __name__ == "__main__":
    Game()