import pygame as pg
import copy
import random


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
        TETRIS_MUSIC = pg.mixer.Sound('sounds/Tetris_theme.mp3')
        TETRIS_MUSIC.set_volume(0.1)

        EXPLODE = pg.mixer.Sound('sounds/explosion.mp3')
        EXPLODE.set_volume(0.4)
        
        HARD_DROP = pg.mixer.Sound('sounds/hard_drop.mp3')
        HARD_DROP.set_volume(0.5)

        ROTATE = pg.mixer.Sound('sounds/rotate.mp3')
        ROTATE.set_volume(0.2)

        SWAP = pg.mixer.Sound('sounds/swap.mp3')
        SWAP.set_volume(0.7)

    class Cooldowns():
        """Class that stores all the cooldown values"""
        PUSH_DOWN = 0.7
        PUSH_SIDE = 0.1
        ROTATE = 0.3
        HARD_DROP = 0.5
        MOVE_MARGIN = 1 # Defines for how long can a player move after the block fell
        REMOVE_ROW = 0.7 # Defines how long will a row say on the map before being removed

    class Game_properties():
        """Class that stores all the game properties"""
        BLOCK_SIZE = 60
        WIDTH = BLOCK_SIZE * 18
        HEIGHT = BLOCK_SIZE * 20
        TICK_RATE = 20
        TITLE = 'Tetris by LSTEP'
        BACKGROUND_COLOR = Colors.BEIGE
        score = 0
        level = 0

class Fonts():
    """Class that stores all the font related information"""
    b_size = Values.Game_properties.BLOCK_SIZE
    pg.font.init()
    TETRIS_FONT = pg.font.SysFont('Tetris', Values.Game_properties.BLOCK_SIZE)
    
    TITLE_SCORE = TETRIS_FONT.render("SCORE", 1, Colors.WHITE)
    score = TETRIS_FONT.render(str(Values.Game_properties.score), 1, Colors.WHITE)
    HOLD = TETRIS_FONT.render('HOLD', 1, Colors.WHITE)
    NEXT = TETRIS_FONT.render('NEXT', 1, Colors.WHITE)
    TITLE_LEVEL = TETRIS_FONT.render('LEVEL', 1, Colors.WHITE)
    level = TETRIS_FONT.render(str(Values.Game_properties.level), 1, Colors.GOLD)

    texts = [(TITLE_SCORE, (b_size/6,b_size*2)), [score, (b_size/6, b_size*3.5)], (HOLD, (b_size/2, b_size*10)), (NEXT, (b_size*14 + b_size/2, b_size*2)), (TITLE_LEVEL, (b_size*14 + b_size/2, b_size*10)), [level, (b_size*15 + b_size*0.75, b_size*12)]]

    def update_text():
        """Method that updates text on the screen"""
        score = Fonts.TETRIS_FONT.render(str(Values.Game_properties.score), 1, Colors.WHITE)
        Fonts.texts[1][0] = score
        level = Fonts.TETRIS_FONT.render(str(Values.Game_properties.level), 1, Colors.GOLD)
        Fonts.texts[5][0] = level

class Timer():
    """Class that tracks all the cooldowns in the game"""
    push_down = -1
    push_side = -1
    rotate = -1
    hard_drop = -1
    swap = -1
    move_margin = -1
    remove_row = -1

    def count():
        """Method that counts and resets the cooldowns"""
        if Timer.push_down != -1:
            Timer.push_down += 1
        if Timer.push_down / Values.Game_properties.TICK_RATE >= Values.Cooldowns.PUSH_DOWN:
            Timer.push_down = -1

        if Timer.push_side != -1:
            Timer.push_side += 1
        if Timer.push_side / Values.Game_properties.TICK_RATE == Values.Cooldowns.PUSH_SIDE:
            Timer.push_side = -1
        
        if Timer.rotate != -1:
            Timer.rotate += 1
        if Timer.rotate / Values.Game_properties.TICK_RATE == Values.Cooldowns.ROTATE:
            Timer.rotate = -1
        
        if Timer.hard_drop != -1:
            Timer.hard_drop += 1
        if Timer.hard_drop / Values.Game_properties.TICK_RATE == Values.Cooldowns.HARD_DROP:
            Timer.hard_drop = -1

        if Timer.move_margin != -1:
            Timer.move_margin += 1
        if Timer.move_margin / Values.Game_properties.TICK_RATE == Values.Cooldowns.MOVE_MARGIN:
            Game.hard_drop()
            Timer.move_margin = -1
        
        if Timer.remove_row != -1:
            Timer.remove_row += 1
        if Timer.remove_row / Values.Game_properties.TICK_RATE == Values.Cooldowns.REMOVE_ROW:
            Game.remove_row(True)
            Values.Sounds.EXPLODE.play()
            Timer.remove_row = -1
            
class Block():
    """Class that stores block methods and blocks of the game"""
    # Lists that store the blocks
    moving_blocks = [] #Blocks that are falling
    static_blocks = [] #Blocks that already fell
    holded_blocks = [] #Blocks that are being "Holded" by the player and can be swapped with the moving blocks
    next_blocks  =  [] #Blocks that will come up next
    ghost_blocks =  []
    blocks_to_delete = []
  
    def __init__(self, x, y, sprite, index, block_type):
        """The init function that stores all the properties of a block object"""
        self.x = x
        self.y = y
        self.sprite = sprite
        self.index = index
        self.block_type = block_type
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)

    def display(self):
        """Displayes the block"""
        self.object = pg.Rect(self.x, self.y, Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE)
        Game.WINDOW.blit(Gui.BLOCK_SPRITES[self.sprite], (self.x, self.y))

    def push_down(self):
        """Moves the block down"""
        self.y += Values.Game_properties.BLOCK_SIZE

    def push_side(self, side):
        """Pushes the block to the sides"""
        if side == 'left':
            self.x -= Values.Game_properties.BLOCK_SIZE
        else:
            self.x += Values.Game_properties.BLOCK_SIZE
    
class Gui():
    """Contains all the graphical user interface related items"""
    left_square = pg.Rect(0,0, Values.Game_properties.BLOCK_SIZE*4, Values.Game_properties.HEIGHT)
    right_square = pg.Rect(Values.Game_properties.BLOCK_SIZE * 14 , 0, Values.Game_properties.BLOCK_SIZE*4, Values.Game_properties.HEIGHT)

    BACKGROUND_SPRITE = pg.image.load('sprites/background.jpg')
    BACKGROUND_SPRITE = pg.transform.rotate(BACKGROUND_SPRITE, 90)
    BACKGROUND_SPRITE = pg.transform.scale(BACKGROUND_SPRITE, (Values.Game_properties.BLOCK_SIZE*10, Values.Game_properties.BLOCK_SIZE*20))

    CYAN_SPRITE = pg.image.load('sprites/cyan_block.png')
    CYAN_SPRITE = pg.transform.scale(CYAN_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    BLUE_SPRITE = pg.image.load('sprites/blue_block.png')
    BLUE_SPRITE = pg.transform.scale(BLUE_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    ORANGE_SPRITE = pg.image.load('sprites/orange_block.png')
    ORANGE_SPRITE = pg.transform.scale(ORANGE_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    PURPLE_SPRITE = pg.image.load('sprites/purple_block.png')
    PURPLE_SPRITE = pg.transform.scale(PURPLE_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    RED_SPRITE = pg.image.load('sprites/red_block.png')
    RED_SPRITE = pg.transform.scale(RED_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    GREEN_SPRITE = pg.image.load('sprites/green_block.png')
    GREEN_SPRITE = pg.transform.scale(GREEN_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    YELLOW_SPRITE = pg.image.load('sprites/yellow_block.png')
    YELLOW_SPRITE = pg.transform.scale(YELLOW_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    GHOST_SPRITE = pg.image.load('sprites/ghost_block.png')
    GHOST_SPRITE = pg.transform.scale(GHOST_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    DELETED_SPRITE = pg.image.load('sprites/deleted_block.png')
    DELETED_SPRITE = pg.transform.scale(DELETED_SPRITE, (Values.Game_properties.BLOCK_SIZE, Values.Game_properties.BLOCK_SIZE))

    BLOCK_SPRITES = [CYAN_SPRITE, BLUE_SPRITE, ORANGE_SPRITE, PURPLE_SPRITE, RED_SPRITE, GREEN_SPRITE, YELLOW_SPRITE, GHOST_SPRITE, DELETED_SPRITE]
        
class Block_types():
      """Stores all the possible block types"""
      block_types = [
        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, 0 , index, '1') for pos_x, pos_y, index in zip([8 for _ in range(4)], [value+1 for value in range(4)], [value+1 for value in range(4)])],
        
        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, 1, index, '2') for pos_x, pos_y, index in zip([8, 8, 8, 9], [1, 2, 3, 3], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, 2, index, '3') for pos_x, pos_y, index in zip([8, 8, 8, 7], [1, 2, 3, 3], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, 3, index, '4') for pos_x, pos_y, index in zip([8, 8, 7, 9], [1, 2, 2, 2], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, 4, index, '5') for pos_x, pos_y, index in zip([7, 8, 8, 9], [2, 2, 1, 1], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, 5, index, '6') for pos_x, pos_y, index in zip([7, 8, 8, 9], [1, 1, 2, 2], [value+1 for value in range(4)])],

        [Block(Values.Game_properties.BLOCK_SIZE * pos_x, -Values.Game_properties.BLOCK_SIZE * pos_y, 6, index, '7') for pos_x, pos_y, index in zip([8, 8, 9, 9], [1, 2, 1, 2], [value+1 for value in range(4)])]
      ]

class Game():
    """Class that contains all the important information and game loop"""
    WINDOW = pg.display.set_mode((Values.Game_properties.WIDTH, Values.Game_properties.HEIGHT))
    pg.display.set_caption(Values.Game_properties.TITLE)

    def __init__(self):
        """Contains the game loop and initializes items connected with it"""
        pg.init()
        Values.Sounds.TETRIS_MUSIC.play(-1)
        self.clock = pg.time.Clock()
        self.run = True
        Block.next_blocks = copy.deepcopy(Block_types.block_types[random.randint(0, len(Block_types.block_types)-1)])
        Game.add_new_blocks()
        while self.run == True:
            self.clock.tick(Values.Game_properties.TICK_RATE)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
            
            if Timer.push_down == -1 and Game.should_fall(Block.moving_blocks): #Pushes the blocks down when the timer reaches -1
                Game.push_down()
                Values.Game_properties.score += 5
                Fonts.update_text()
                Timer.push_down = 0

            Game.controls()
            Game.adjust_difficulty()
            Game.remove_blocks()
            Game.remove_row()
            Game.place_ghost_blocks()
            Game.visuals()
            Timer.count()
            

    def visuals():
        """Responsible for drawing all the objects on the screen"""
        Game.WINDOW.fill(Values.Game_properties.BACKGROUND_COLOR)
        Game.WINDOW.blit(Gui.BACKGROUND_SPRITE, (Values.Game_properties.BLOCK_SIZE*4, 0))
      
        pg.draw.rect(Game.WINDOW, Colors.BLACK, Gui.left_square)
        pg.draw.rect(Game.WINDOW, Colors.BLACK, Gui.right_square)

        for text, coordinates in Fonts.texts:
            Game.WINDOW.blit(text, coordinates)

        for block in Block.ghost_blocks:
            if Timer.move_margin == -1:
                block.display()
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
            b_size = Values.Game_properties.BLOCK_SIZE

            Block.moving_blocks = copy.deepcopy(Block_types.block_types[int(Block.next_blocks[0].block_type)-1]) # Places block of the same type as the one in next_blocks on the board
            Block.next_blocks = []
            Block.next_blocks = copy.deepcopy(Block_types.block_types[random.randint(0, len(Block_types.block_types)-1)]) # Randomizes a block to add to the next_blocks
            for block in Block.next_blocks: # Takes the blocks from next_blocks and puts them in the same place
                block.x, block.y = (b_size*15, b_size*4)
            Game.recreate_shape(Block.next_blocks) # Recreates the shape of the block

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
        
        if keys_pressed[pg.K_SPACE] and Timer.hard_drop == -1:
            Game.hard_drop()
        
    def remove_blocks(remove = False):
        """Moves the blocks into static list when they fall and adds new blocks"""
        if remove:
            Block.static_blocks += Block.moving_blocks 
            Block.moving_blocks = []
            Game.add_new_blocks()
            Timer.swap = -1
            return

        if not Game.should_fall(Block.moving_blocks) and Timer.move_margin == -1:
            Timer.move_margin = 0

    def remove_row(remove = False):
        """Checks if a row is filled, removes the blocks, and pushes other down"""
        y_values = list(reversed([Values.Game_properties.BLOCK_SIZE * value for value in range(20)])) # List of all Y-values on the screen
        
        for y_value in y_values: # Iterates through each Y-value
            num_of_blocks = 0

            for block in Block.static_blocks: # Checks how many blocks are in a row
                if block.y == y_value:
                    num_of_blocks += 1

            if num_of_blocks == 10: # If the row is full it selects the blocks of the row and appends them to the Block.blocks_to_delete list
                for block in Block.static_blocks:
                    if block.y == y_value and block.sprite != 8:
                        block.sprite = 8
                        Block.blocks_to_delete.append(block)
                        Timer.remove_row = 0

        if remove:
            for block in Block.blocks_to_delete: # Removes the blocks from the static list
                    Block.static_blocks.remove(block)
                    Values.Game_properties.score += len(Block.blocks_to_delete) * 2

            if Block.blocks_to_delete: # If The Y-Value of a block is lower than the Y-value of the row it moves the block down
                for block in Block.static_blocks:
                    if block.y < Block.blocks_to_delete[0].y:
                        block.y += Values.Game_properties.BLOCK_SIZE * (len(Block.blocks_to_delete) / 10)
            Block.blocks_to_delete = []

    def rotate():
        """Rotates the block"""
        Values.Sounds.ROTATE.play()

        if Block.moving_blocks[0].sprite != 6:
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
            Game.out_of_bounds()

    def should_move(x_cor, side):
        """Checks if a block can move to the side"""
        for block in Block.moving_blocks:
            if side == 'left':
                if block.x - x_cor < Values.Game_properties.BLOCK_SIZE * 4:
                    return False
                for static_block in Block.static_blocks:
                    if block.x - Values.Game_properties.BLOCK_SIZE == static_block.x and block.y == static_block.y:
                        return False
            if side == 'right':
                if block.x + x_cor > Values.Game_properties.BLOCK_SIZE * 13:
                    return False
                for static_block in Block.static_blocks:
                    if block.x + Values.Game_properties.BLOCK_SIZE == static_block.x and block.y == static_block.y:
                        return False
        return True

    def recreate_shape(container):
        b_size = Values.Game_properties.BLOCK_SIZE
        match container[0].block_type: # Translates the blocks to their shapes
            case '1':
                for block, coordinates in zip(container, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*0, b_size*2), (b_size*0, b_size*3)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '2':
                for block, coordinates in zip(container, [(b_size*1, b_size*0), (b_size*1, b_size*1), (b_size*1, b_size*2), (b_size*0, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '3':
                for block, coordinates in zip(container, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*0, b_size*2), (b_size*1, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '4':
                for block, coordinates in zip(container, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*0, b_size*2), (b_size*1, b_size*1)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '5':
                for block, coordinates in zip(container, [(b_size*1, b_size*0), (b_size*0, b_size*1), (b_size*1, b_size*1), (b_size*0, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '6':
                for block, coordinates in zip(container, [(b_size*0, b_size*0), (b_size*0, b_size*1), (b_size*1, b_size*1), (b_size*1, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y
            case '7':
                for block, coordinates in zip(container, [(b_size*0, b_size*1), (b_size*1, b_size*1), (b_size*0, b_size*2), (b_size*1, b_size*2)]):
                    x, y = coordinates
                    block.x += x
                    block.y += y

    def swap():
        """Swaps the blocks between moving and holded list"""
        Values.Sounds.SWAP.play()
        
        temporary = []
        
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

        Game.recreate_shape(Block.holded_blocks)

        if len(Block.moving_blocks) == 0: # If moving blocks is empty it adds blocks to it
            Game.add_new_blocks()

    def adjust_difficulty():
        for score, cooldown, level in ((5000, 0.6, 1), (10000, 0.5, 2), (15000, 0.4, 3), (25000, 0.35, 4), (35000, 0.3, 5), (45000, 0.25, 6), (55000, 0.2, 7), (70000, 0.15, 8), (100000, 0.1, 9), (150000, 0.05, 10)):
            if Values.Game_properties.score >= score:
                Values.Cooldowns.PUSH_DOWN = cooldown
                Values.Game_properties.level = level

    def place_ghost_blocks():
        Block.ghost_blocks = copy.deepcopy(Block.moving_blocks)
        repeat = True
        while repeat:
            if not Game.should_fall(Block.ghost_blocks):
                return
            for block in Block.ghost_blocks:
                block.sprite = 7
                block.push_down()

    def hard_drop():
        Values.Sounds.HARD_DROP.play()
        repeat = True
        while repeat:
            Values.Game_properties.score += 12
            if not Game.should_fall(Block.moving_blocks):
                repeat = False
            if repeat == True:
                for block in Block.moving_blocks:
                    block.push_down()
        Timer.hard_drop = 0
        Timer.move_margin = -1
        Game.remove_blocks(True)
        
    def should_fall(container):
        should_fall = True
        for block in container:
            if block.y + Values.Game_properties.BLOCK_SIZE == Values.Game_properties.HEIGHT:
                should_fall = False
            for static_block in Block.static_blocks:
                if block.y + Values.Game_properties.BLOCK_SIZE == static_block.y and block.x == static_block.x:
                    should_fall = False
        return should_fall
    
    def out_of_bounds(repeat = True):
        b_size = Values.Game_properties.BLOCK_SIZE
        move_x = 0

        for block in Block.moving_blocks:
            if block.x < b_size*4:
                move_x = b_size
            if block.x > b_size*13:
                move_x = -b_size
        
        for block in Block.moving_blocks:
            block.x += move_x

        if move_x != 0 and Block.moving_blocks[0].sprite == 0 and repeat:
            Game.out_of_bounds(False)
            print('a')


if __name__ == "__main__": # Runs the game if run from the main file
    Game()