import pygame
import math
import random
import sys
from queue import PriorityQueue


# width of window
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Game.")


# our colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# keep tracks of the tiles in our grid
class Spot:
    def __init__(self, row, col, width, total_rows):
        #the row the tile is in
        self.row = row
        # the column the tile is in
        self.col = col
        # the x-coordinate the tile is in (depends on the width of the tile)
        self.x = row * width
        # the y-coordinate the tile is in (depends on the width of the tile)
        self.y = col * width
        # the color of the tile
        self.color = WHITE
        # the tile neighbors. Only store the neighbors where an enemy can move onto (an empty tile or a character tile)
        self.neighbors = []
        # width of a tile
        self.width = width
        #the amount of rows in the grid
        self.total_rows = total_rows

    #returns position
    def get_pos(self):
        return self.row, self.col



    #checks if a tile is a certain tile
    def is_barrier(self):
        return self.color == BLACK

    def is_character(self):
        return self.color == ORANGE

    def is_portal(self):
        return self.color == PURPLE

    def is_enemy(self):
        return self.color == BLUE

    def is_blank(self):
        return self.color == WHITE
    def is_flag(self):
        return self.color == YELLOW

    # sets a tile's status
    def reset(self):
        self.color = WHITE

    def make_character(self):
        self.color = ORANGE

    def make_barrier(self):
        self.color = BLACK

    def make_portal(self):
        self.color = PURPLE

    def make_enemy(self):
        self.color = BLUE

    def make_flag(self):
        self.color = YELLOW

    #draw a tile
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # checks if a tile is an empty tile or character (only used in update_neighbors)
    def valid_neighbor(self,x,y,grid):

        if  grid[self.row + x][self.col+y].is_character() or grid[self.row + x][self.col+y].is_blank():
            return True
        return False

    #only used to control the enemies (blue tile). If a blue tile can move to this tile, then it is stored in the neighbor list
    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and self.valid_neighbor(1,0,grid)  :  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0  and self.valid_neighbor(-1,0,grid) :  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1  and self.valid_neighbor(0,1,grid) :  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and  self.valid_neighbor(0,-1,grid):  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


    #  lt=less than. so self is always greater than other. We use this for the comparison but this always return false so not really accurate
    def __lt__(self, other):
        return False


# distance between point one and point two
# taxi cab distance - we find the exact difference between one point and another ignoring everything else
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)



# makes a grid
def make_grid(rows, width):
    grid = []
    # gap - gap between each rows
    gap = width // rows

    for i in range(rows):

        # makes a 2d list
        grid.append([])

        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

#draws the grid, win is the window
def draw_grid(win, rows, width):

    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# redraw every 10 seconds
def draw(win, grid, rows, width):


    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


#enemy goes to the next adjacent spot that brings them closer to the player
def go_though_path(came_from,current,draw):
    if came_from:
        #stay in place if an enemy is in front
        temp=came_from[current]
        if not temp.is_enemy():
            current.reset()
            temp.make_enemy()
            draw()
            return temp
        else:
            #stay in place
            return current


# the algorithm to determine the best path from an enemy to a player
#draw - the draw function
#grid - the entire grid
#start - the tile where we want to start
#end - the tile where we want to go
#makepath - a boolean function that determines if we want the tile in 'start' to move or not
# the way the algorithm works is we can a g and h score. The g score is determined by
#how much tiles from the start position a tile is. the f score is the taxi-cab difference (defined in function h)
# we want the lowest value
def algorithm(draw, grid, start, end,makepath):

    #count is used to break ties if two tiles have the same score
    count = 0
    # all the tiles we are considering
    open_set = PriorityQueue()

    # 0 is f score, count - break ties if two values had the same score, just pick the first one, start is the node
    open_set.put((0, count, start))

    #stores where each tile came from
    came_from = {}

    #stores the g scores ()
    g_score = {spot: float("inf") for row in grid for spot in row}

    g_score[start] = 0
    #stores the f score
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # this  will have everything the  priority queue has but now you can check what it has  (in priority queue you can't )
    open_set_hash = {start}

    #continues if their is still a node to be evaluated
    while not open_set.empty():

        #quit if user quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        #  the  2 gets the node (the third value)
        current = open_set.get()[2]
        open_set_hash.remove(current)

        #  when we find the path
        if current == end:

            # if makepath is true, move the enemy, otherwise return true
            if makepath:
                end = go_though_path(came_from, end, draw)
                return end

            return True




        for neighbor in current.neighbors:
            #increments the g_score by 1 for every new tile
            temp_g_score = g_score[current] + 1
            #  if found a better way to get here, store it
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                # put neighbor in the list
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)


        draw()


    #return false if there is no path
    return False



#determines if the player can pass through it's neighbour tile
def passthrough(neighbour):
    if not neighbour.is_barrier():
        return True
    return False

#displays text. Used for the winner and loser message
def display_text(text):
    pygame.init()
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    X = 400
    Y = 400

    # create the display surface object
    # of specific dimension..e(X, Y).
    display_surface = pygame.display.set_mode((X, Y))

    # set the pygame window name
    pygame.display.set_caption(text)

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 32)

    # create a text suface object,
    # on which text is drawn on it.
    text = font.render(text, True, green, white)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (X // 2, Y // 2)

    # infinite loop
    while True:

        # completely fill the surface object
        # with white color
        display_surface.fill(white)

        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        display_surface.blit(text, textRect)

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

            # Draws the surface object to the screen.
            pygame.display.update()




#main program that is responsible for starting the game
def startgame(win, width):

    # number of rows in a grid
    ROWS = 30
    grid = make_grid(ROWS, width)



    #places 250 walls randomly
    for x in range(0,250):
        temp=False
        while(not temp):
            number=random.randint(0, 29)
            number2 = random.randint(0, 29)
            if(grid[number][number2].is_blank()):
                grid[number][number2].make_barrier()
                temp=True

    #update each tile's neighbor by saying if anyone can move to that space. Checks if neighbors are walls
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)


    #places the yellow wall (the objectives)
    objective1=None
    objective2=None
    objective3=None
    objectiveList = [objective1, objective2, objective3]
    objectivePlaced = False
    objective1P= False
    objective2P = False
    objective3P = False

    #places the objectives randomly, then check if there is a path that can reach all 3 objectives. We want
    #to make sure all objectives are reachable and are not stuck in a wall
    while not objectivePlaced:
        while not objective1P:
            flag1X=random.randint(0, ROWS-1)

            flag1Y = random.randint(0, ROWS-1)
            if not grid[flag1X][flag1Y].is_barrier():
                objective1= grid[flag1X][flag1Y]
                objective1P=True
        while not objective2P:
            flag1X = random.randint(0, ROWS - 1)
            flag1Y = random.randint(0, ROWS - 1)
            if not grid[flag1X][flag1Y].is_barrier():
                objective2 = grid[flag1X][flag1Y]
                objective2P = True
        while not objective3P:
            flag1X = random.randint(0, ROWS - 1)
            flag1Y = random.randint(0, ROWS - 1)
            if not grid[flag1X][flag1Y].is_barrier():
                objective3 = grid[flag1X][flag1Y]
                objective3P = True




        #if there is a path from flag 1 to flaga 2, and a path from flag 1 to flag 3, there is a path to flag 2 to flag 3
        if algorithm(lambda: draw(win, grid, ROWS, width), grid, objective1, objective2, False) and algorithm(lambda: draw(win, grid, ROWS, width), grid, objective1, objective3, False):

            objectivePlaced=True
        else:
            print("problem")


        objective1P=False
        objective2P = False
        objective3P = False


    objective1.make_flag()
    objective2.make_flag()
    objective3.make_flag()



    #the x and y coordinate of the player (we refer to as start)
    playerX=0
    playerY=0
    playerPlaced=False

    while not playerPlaced:
        playerX=random.randint(0, ROWS - 1)
        playerY = random.randint(0, ROWS - 1)
        start=grid[playerX][playerY]
        if start.is_blank():
            # if we have a path to flag1 from our character, and there is a path from flag1 to flag2 and flag3, then there is a path from our character to flag 2 and flag 3
            if algorithm(lambda: draw(win, grid, ROWS, width), grid, start, objective1, False) :
                playerPlaced=True

    start.make_character()


    #places portal and make sure user can reach it
    portal1Placed = False
    portal1 = None
    while (not portal1Placed):
        portal1 = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if portal1.is_blank() and algorithm(lambda: draw(win, grid, ROWS, width), grid, start, portal1, False):
            portal1Placed = True

    portal1.make_portal()
    # places portal and make sure user can reach it
    portal2Placed = False

    portal2 = None
    while (not portal2Placed):
        portal2 = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if portal2.is_blank() and algorithm(lambda: draw(win, grid, ROWS, width), grid, start, portal2, False):
            portal2Placed = True

    portal2.make_portal()

    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)


    #places enemy and make sure enemy can reach player
    enemy1=None
    enemy2 = None
    enemy3 = None


    enemy1Placed=False

    while(not enemy1Placed):

        enemy1=grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]

        if enemy1.is_blank() and algorithm(lambda: draw(win, grid, ROWS, width), grid, start, enemy1, False):
            enemy1Placed=True

    enemy1.make_enemy()
    enemy2Placed = False

    while (not enemy2Placed):
        enemy2 = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if enemy2.is_blank() and algorithm(lambda: draw(win, grid, ROWS, width), grid, start, enemy2, False):
            enemy2Placed = True

    enemy2.make_enemy()

    enemy3Placed = False

    while (not enemy3Placed):
        enemy3 = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if enemy3.is_blank() and algorithm(lambda: draw(win, grid, ROWS, width), grid, start, enemy3, False):
            enemy3Placed = True

    enemy3.make_enemy()


    #the lists of the portal,enemies and objectives
    portalList=[portal1,portal2]
    enemyList = [enemy1, enemy2, enemy3]
    objectiveList=[objective1,objective2,objective3]
    #what is turned to a wall
    turntowall=[]



    #when runs become false, stop running the program
    run = True
    #determines if it is the opponents turn or not
    enemyTurn =  False
    while run:
        draw(win, grid, ROWS, width)
        # whenever an event happens, if timer runs out, if user clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                run = False




            if event.type == pygame.KEYDOWN:
                # press a key down, move character down
                if event.key == pygame.K_DOWN and  playerY>=0  and playerY<ROWS -1 and passthrough(grid[playerX][playerY+1]):
                    start.reset()
                    playerY=playerY+1
                    start=grid[playerX][playerY]
                    start.make_character()
                    enemyTurn=True
                # press a key up, move character up
                if event.key == pygame.K_UP and  playerY>0  and playerY<=ROWS -1 and passthrough(grid[playerX][playerY-1]):
                    start.reset()
                    playerY=playerY-1
                    start=grid[playerX][playerY]
                    start.make_character()
                    enemyTurn = True

                # press a key right, move character right
                if event.key == pygame.K_RIGHT and  playerX>=0  and playerX<ROWS -1 and passthrough(grid[playerX+1][playerY]):
                    start.reset()
                    playerX=playerX+1
                    start=grid[playerX][playerY]
                    start.make_character()
                    enemyTurn = True

                # press a key left, move character left
                if event.key == pygame.K_LEFT and playerX > 0 and playerX <= ROWS - 1 and passthrough(grid[playerX-1][playerY]):

                    start.reset()
                    playerX = playerX - 1
                    start = grid[playerX][playerY]
                    start.make_character()
                    enemyTurn = True


        if enemyTurn:

            # if enemy is on the player tile, then display that they lost
            for x in enemyList:
                if start == x:
                    display_text("You Lost")


            # if their is anything to turn into a wall (a tile that was previously a portal or an objective), then turn it into a wall
            for x in turntowall:
                x.make_barrier()
                turntowall.remove(x)

            #if the player is on a yellow wall, remove it from the flag list and turn it into a wall
            for x in objectiveList:
                if start == x:
                    objectiveList.remove(x)
                    turntowall.append(x)

            # if the flag list is empty, display they won
            if not objectiveList:
                display_text("You Won")


            # if they are on a portal, transport them to a random empty sot
            for x in portalList:
                if start == x:
                    bool = False
                    while not bool:
                        playerX = random.randint(0, ROWS - 1)
                        playerY = random.randint(0, ROWS - 1)
                        if grid[playerX][playerY].is_blank():
                            start.reset()
                            start = grid[playerX][playerY]
                            start.make_character()
                            bool = True
                            x.make_barrier()

            for x in range(0,len(enemyList)):
                #move the enemies
                enemyList[x]=algorithm(lambda: draw(win, grid, ROWS, width), grid, start, enemyList[x],True)
                if enemyList[x]==start or enemyList[x]==False:
                    #if enemy on player, they win
                    display_text("You Lost")



            enemyTurn=False

    pygame.quit()

startgame(WIN, WIDTH)
