import pygame as pg
import copy
import random
import time


class Colors():
    """Class that contains all the most common colors"""
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
    """Class that stores all basic values"""
    class Sounds():
        """Class that stores all the audio"""
        pg.mixer.init(44100, -16,2,2048)
        TETRIS_MUSIC = pg.mixer.Sound('Tetris_theme.mp3')

    class Cooldown():
        """Class that stores all the cooldown values"""
        PUSH_DOWN_COOLDOWN = 0.5
        PUSH_SIDE_COOLDOWN = 0.1
        ROTATE_COOLDOWN = 0.3
        SWAP_COOLDOWN = 1

    class Game_properties():
        """Class that stores all the game properties"""
        BLOCK_SIZE = 60
        WIDTH = BLOCK_SIZE * 18
        HEIGHT = BLOCK_SIZE * 20
        TICK_RATE = 30
        TITLE = 'Tetris by LSTEP'
        BACKGROUND_COLOR = Colors.BEIGE
        score = 0

class Fonts():
    """Class that stores all the font related information"""
    b_size = Values.Game_properties.BLOCK_SIZE
    pg.font.init()
    SCORE = pg.font.SysFont('Tetris', Values.Game_properties.BLOCK_SIZE)
    
    TITLE_SCORE = SCORE.render("SCORE", 1, Colors.WHITE)
    score = SCORE.render(str(Values.Game_properties.score), 1, Colors.WHITE)
    HOLD = SCORE.render('HOLD', 1, Colors.WHITE)
    NEXT = SCORE.render('NEXT', 1, Colors.WHITE)

    texts = [(TITLE_SCORE, (b_size/6,b_size*2)), [score, (b_size/6, b_size*3.5)], (HOLD, (b_size/2, b_size*10)), (NEXT, (b_size*14 + b_size/2, b_size))]

    def update_score():
        """Method that updates the score on the screen"""
        score = Fonts.SCORE.render(str(Values.Game_properties.score), 1, Colors.WHITE)
        Fonts.texts[1][0] = score

class Timer():
    """Class that tracks all the cooldowns in the game"""
    push_down = -1
    push_side = -1
    rotate = -1
    swap = -1

    def count():
        """Method that counts and resets the cooldowns"""
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
        
        if Timer.swap != -1:
            Timer.swap += 1
        if Timer.swap / Values.Game_properties.TICK_RATE == Values.Cooldown.SWAP_COOLDOWN:
            Timer.swap = -1



class Block():
    """Class that stores block methods and blocks of the game"""
    # Lists that store the blocks
    moving_blocks = [] #Blocks that are falling
    static_blocks = [] #Blocks that already fell
    holded_blocks = [] #Blocks that are being "Holded" by the player and can be swapped with the moving blocks
    next_blocks  =  [] #Blocks that will come up next
  
    def __init__(self, x, y, color, index, block_type):
        """The init function that stores all the properties of a block object"""
        self.x = x
        self.y = y
        self.color = color
        self.index = index
        self.block_type = block_type
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)

    def display(self):
        """Displayes the block"""
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)
        pg.draw.rect(Game.WINDOW, self.color, self.object)

    def push_down(self):
        """Moves the block down"""
        self.y += Values.Game_properties.BLOCK_SIZE
    
    def should_fall(self):
        """Checks if the block should fall"""
        if self.y + Values.Game_properties.BLOCK_SIZE == Values.Game_properties.HEIGHT:
            return True
        for block in Block.static_blocks:
            if self.y + Values.Game_properties.BLOCK_SIZE == block.y and self.x == block.x:
                return True
        return False

    def push_side(self, side):
        """Pushes the block to the sides"""
        if side == 'left':
            self.x -= Values.Game_properties.BLOCK_SIZE
        else:
            self.x += Values.Game_properties.BLOCK_SIZE
    

        

class Block_types():
      """Stores all the possible block types"""
      block_types = [
        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.CYAN, index, '1') for pos_x, pos_y, index in zip([8 for _ in range(4)], [value+1 for value in range(4)], [value+1 for value in range(4)])],
        
        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.BLUE, index, '2') for pos_x, pos_y, index in zip([8, 8, 8, 9], [1, 2, 3, 3], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.ORANGE, index, '3') for pos_x, pos_y, index in zip([8, 8, 8, 7], [1, 2, 3, 3], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.PURPLE, index, '4') for pos_x, pos_y, index in zip([8, 8, 7, 9], [1, 2, 2, 2], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.RED, index, '5') for pos_x, pos_y, index in zip([7, 8, 8, 9], [2, 2, 1, 1], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.GREEN, index, '6') for pos_x, pos_y, index in zip([7, 8, 8, 9], [1, 1, 2, 2], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, Colors.YELLOW, index, '7') for pos_x, pos_y, index in zip([8, 8, 9, 9], [1, 2, 1, 2], [value+1 for value in range(4)])]
      ]

class Gui():
    """Contains all the graphical user interface related items"""
    left_square = pg.Rect(0,0, Values.Game_properties.BLOCK_SIZE*4, Values.Game_properties.HEIGHT)
    right_square = pg.Rect(Values.Game_properties.BLOCK_SIZE * 14 , 0, Values.Game_properties.BLOCK_SIZE*4, Values.Game_properties.HEIGHT)


class Game():
    """Class that contains all the important information and game loop"""
    WINDOW = pg.display.set_mode((Values.Game_properties.WIDTH, Values.Game_properties.HEIGHT))
    pg.display.set_caption(Values.Game_properties.TITLE)

    def __init__(self):
        """Contains the game loop and initializes items connected with it"""
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
            
            if Timer.push_down == -1: #Pushes the blocks down when the timer reaches -1
                Game.push_down()
                Values.Game_properties.score += 5
                Fonts.update_score()
                Timer.push_down = 0

            Game.controls()
            Game.remove_blocks()
            Game.remove_row()
            Game.visuals()
            Timer.count()
            

    def visuals():
        """Responsible for drawing all the objects on the screen"""
        Game.WINDOW.fill(Values.Game_properties.BACKGROUND_COLOR)
      
        pg.draw.rect(Game.WINDOW, Colors.BLACK, Gui.left_square)
        pg.draw.rect(Game.WINDOW, Colors.BLACK, Gui.right_square)

        for text, coordinates in Fonts.texts:
            Game.WINDOW.blit(text, coordinates)

        for block in Block.moving_blocks:
            block.display()
        for block in Block.static_blocks:
            block.display()
        for block in Block.holded_blocks:
            block.display()
        for block in Block.next_blocks:
            block.display()

        pg.display.update()

    def push_down():
        """Pushes the blocks one tile down"""
        for block in Block.moving_blocks:
            block.push_down()

    def add_new_blocks(index=None):
        """Adds one of the seven blocks to the game, can be randomized or a specific block"""
        if index == None:
            random.seed(time.time())
            Block.moving_blocks = copy.deepcopy(Block_types.block_types[random.randint(0, len(Block_types.block_types)-1)])
        else:
            Block.moving_blocks = copy.deepcopy(Block_types.block_types[index])


    def controls():
        """Gathers information about keys pressed and runs the associated functions"""
        keys_pressed = pg.key.get_pressed() #Stores all the info in a list
        
        # Moves the blocks to the left
        if keys_pressed[pg.K_a] and Timer.push_side == -1:
            if Game.should_move(Values.Game_properties.BLOCK_SIZE, 'left'):
                for block in Block.moving_blocks:
                    block.push_side("left")
            Timer.push_side = 0
        
        # Moves blocks to the right
        if keys_pressed[pg.K_d] and Timer.push_side == -1:
            if Game.should_move(Values.Game_properties.BLOCK_SIZE, 'right'):  
                for block in Block.moving_blocks:  
                    block.push_side("right")
            Timer.push_side = 0
        
        # Speeds up the falling of the blocks
        if keys_pressed[pg.K_s] and Timer.push_down != -1:
            Timer.push_down = -1
            Values.Game_properties.score += 5
        
        # Rotates the blocks
        if keys_pressed[pg.K_w] and Timer.rotate == -1:
            Game.rotate()
            Timer.rotate = 0
        
        # Swaps the blocks between moving_blocks and holded_blocks
        if keys_pressed[pg.K_c] and Timer.swap == -1:
            Game.swap()
            Timer.swap = 0

    def remove_blocks():
        """Moves the blocks into static list when they fall and adds new blocks"""
        for block in Block.moving_blocks:
            if block.should_fall():
                Block.static_blocks += Block.moving_blocks 
                Block.moving_blocks = []
                Game.add_new_blocks()
                break

    def remove_row():
        """Checks if a row is filled, removes the blocks, and pushes other down"""
        y_values = list(reversed([Values.Game_properties.BLOCK_SIZE * value for value in range(20)])) # List of all Y-values on the screen

        for y_value in y_values: # Iterates through each Y-value
            blocks_to_remove = []
            num_of_blocks = 0

            for block in Block.static_blocks: # Checks how many blocks are in a row
                if block.y == y_value:
                    num_of_blocks += 1

            if num_of_blocks == 10: # If the row is full it selects the blocks of the row and appends them to the blocks_to_remove list
                for block in Block.static_blocks:
                    if block.y == y_value:
                        blocks_to_remove.append(block)

            for block in blocks_to_remove: # Removes the blocks from the static list
                    Block.static_blocks.remove(block)

            if blocks_to_remove: # If The Y-Value of a block is lower than the Y-value of the row it moves the block down
                for block in Block.static_blocks:
                    if block.y < y_value:
                        block.y += Values.Game_properties.BLOCK_SIZE

    def rotate():
        """Rotates the block"""
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

    def should_move(x_cor, side):
        """Checks if a block can move to the side"""
        for block in Block.moving_blocks:
            if side == 'left':
                if block.x - x_cor < Values.Game_properties.BLOCK_SIZE * 4:
                    return False
            if side == 'right':
                if block.x + x_cor > Values.Game_properties.BLOCK_SIZE * 13:
                    return False
        return True

    def swap():
        """Swaps the blocks between moving and holded list"""
        temporary = []
        b_size = Values.Game_properties.BLOCK_SIZE
        
        for block in Block.moving_blocks: # Copies the moving block list
            temporary.append(block)
        Block.moving_blocks = []

        if len(Block.holded_blocks) != 0: # If the holded blocks list is not empty it moves it's contents to moving blocks list
            Game.add_new_blocks(int(Block.holded_blocks[0].block_type)-1)
        Block.holded_blocks = []

        for block in temporary: # Moves all the blocks into one place to the side of the map
            Block.holded_blocks.append(block)
            block.x = Values.Game_properties.BLOCK_SIZE
            block.y = Values.Game_properties.BLOCK_SIZE * 12

        match Block.holded_blocks[0].block_type: # Translates the blocks to their shapes
            case '1':
                for block, coordinates in zip(Block.holded_blocks, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*0, b_size*2), (b_size*0, b_size*3)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '2':
                for block, coordinates in zip(Block.holded_blocks, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*0, b_size*2), (b_size*1, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '3':
                for block, coordinates in zip(Block.holded_blocks, [(b_size*1, b_size*0), (b_size*1, b_size*1), (b_size*1, b_size*2), (b_size*0, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '4':
                for block, coordinates in zip(Block.holded_blocks, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*0, b_size*2), (b_size*1, b_size*1)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '5':
                for block, coordinates in zip(Block.holded_blocks, [(b_size*1, b_size*0), (b_size*0, b_size*1), (b_size*1, b_size*1), (b_size*0, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '6':
                for block, coordinates in zip(Block.holded_blocks, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*1, b_size*1), (b_size*1, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '7':
                for block, coordinates in zip(Block.holded_blocks, [(b_size*0, b_size*1), (b_size*1, b_size*1), (b_size*0, b_size*2), (b_size*1, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y

        if len(Block.moving_blocks) == 0: # If moving blocks is empty it adds blocks to it
            Game.add_new_blocks()

if __name__ == "__main__": # Runs the game if run from the main file
    Game()