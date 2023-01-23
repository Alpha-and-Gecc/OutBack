#OutBack(rooms)
#Alpha, Gec master and nyaw ‹𝟹
#(Aaron and Lucas)

import pygame as pg
import numpy as np
import random

# Creating player
class Player:
    # Creation code
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Creating enemie
class Enemy:
    # Creation code
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_maze(maze_size, start_side, end_side, num_enemies):
    # Initialize the maze with all walls
    maze = [[1 for _ in range(maze_size * 2 + 1)] for _ in range(maze_size * 2 + 1)]
    for x in range(1, maze_size * 2 + 1, 2):
        for y in range(1, maze_size * 2 + 1, 2):
            maze[x][y] = 0
    start_x, start_y = None, None
    end_x, end_y = None, None
    if start_side == 'top':
        start_x, start_y = 1, random.randint(1, maze_size)
    elif start_side == 'bottom':
        start_x, start
    # Start the depth-first search algorithm at the start point
    stack = [(start_x, start_y)]
    visited = set()
    while stack:
        # Get the current cell from the stack
        x, y = stack[-1]

        # Mark the current cell as visited
        visited.add((x, y))

        # Check the neighboring cells
        neighbors = []
        if x > 1 and (x - 2, y) not in visited:
            neighbors.append((x - 2, y))
        if x < maze_size * 2 - 1 and (x + 2, y) not in visited:
            neighbors.append((x + 2, y))
        if y > 1 and (x, y - 2) not in visited:
            neighbors.append((x, y - 2))
        if y < maze_size * 2 - 1 and (x, y + 2) not in visited:
            neighbors.append((x, y + 2))

        # If there are any unvisited neighboring cells, pick one at random
        # and push it to the stack
        if neighbors:
            next_cell = random.choice(neighbors)
            stack.append(next_cell)

            # Remove the wall between the current cell and the next cell
            dx, dy = next_cell[0] - x, next_cell[1] - y
            maze[x + (dx // 2)][y + (dy // 2)] = 0
        else:
            # If there are no unvisited neighboring cells, backtrack
            stack.pop()

    # remove walls between start and end points
    if start_x == 1:
        maze[start_x][start_y] = 0
    elif start_x == maze_size * 2 - 1:
        maze[start_x][start_y] = 0
    elif start_y == 1:
        maze[start_x][start_y] = 0
    elif start_y == maze_size * 2 - 1:
        maze[start_x][start_y] = 0
    if end_x == 1:
        maze[end_x][end_y] = 0
    elif end_x == maze_size * 2 - 1:
        maze[end_x][end_y] = 0
    elif end_y == 1:
        maze[end_x][end_y] = 0
    elif end_y == maze_size * 2 - 1:
        maze[end_x][end_y] = 0

    # Create player and enemies
    player = Player(start_x, start_y)
    enemies = []
    for i in range(num_enemies):
        enemy_x, enemy_y = random.randint(1, maze_size * 2 - 1), random.randint(1, maze_size * 2 - 1)
        while (enemy_x, enemy_y) in visited:
            enemy_x, enemy_y = random.randint(1, maze_size * 2 - 1), random.randint(1, maze_size * 2 - 1)
        enemies.append(Enemy(enemy_x, enemy_y))

    # Place player and enemies in the maze
    maze[player.x][player.y] = 'P'
    for enemy in enemies:
        maze[enemy.x][enemy.y] = 'E'

    return maze

#TODO: FIX WALLS
def main(map):
    pg.init()
    window = pg.display.set_mode((1600, 1200))
    running = True
#    clock = pg.time.Clock()

    hres = 360#horizontal resolution, must be a multiple of 120
    halfvres = 200#half of the vertical resolution, must be a multiple of 100 that is divisible by hres
    vres = 300#actual full vertical resolution
    fov = 60
    #ackshually it's both fov and camera height

    mod = hres/fov
    #pixels per degree, horizontal
    posX = 0
    posY = 0
    #player coords
    yaw = 0
    #player angle deviation from 0
    frame = np.random.uniform(0, 1, (hres, halfvres*2, 3))
    #textureless texture, randomely generated

    sky = pg.image.load('skybox.jpg')
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres * 2))) / 255
    floor = pg.surfarray.array3d(pg.image.load('floor.jpg')) / 255
    wall = pg.surfarray.array3d(pg.image.load('floor.jpg')) / 255
    #loads images from the project folder

    while vres < halfvres*2:
        vres += 10

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
                #runs the game

        for i in range(hres):
            """get every column of pixels between -fov/2 and +fov/2"""
            columnAngle = yaw + np.deg2rad(i/mod - (fov/2))
            sin = np.sin(columnAngle)
            cos = np.cos(columnAngle)
            #gets the location coordinate of this particular column
            adjustCos = np.cos(np.deg2rad(i/mod - (fov/2)))
            # variable to prevent warping
            #frame[i][:] == floor[int(np.rad2deg(columnAngle)%99)][:]

            for p in range(vres):
                """for every column of pixels, find the colour of each pixel in said column from the bottom up"""
                n = ((halfvres*2)/(vres-p))/adjustCos
                #determines the distance from the player's coordinates to the target pixel
                pixelX = posX + cos*n
                pixelY = posY + sin*n
                #determines the location of said pixel in the camera in relation to the player location

                amendedX = int(pixelX * 2 % 1 * 99)
                amendedY = int(pixelY * 2 % 1 * 99)
                #converts pixel coordinates to int such that it can be found on the textures

                shade = 0.1 + 0.1 * (1 - p / (vres/2))
                #light strength plus max brightness value times the base floor pixel colour

                if map[int(pixelX)%len(map)][int(pixelY%len(map))] == 1:
                    wallheight = halfvres - p
                    paint = shade*np.ones(3)
                    for k in range(wallheight*2):
                        frame[i][halfvres - wallheight + k] = paint
                    break

                else:
                    frame[i][halfvres * 2 - p - 1] = shade*floor[amendedX][amendedY]
                    #renders the pixel at the right colour



#        frame = new_frame(posX, posY, rot, frame, hres, halfvres, mod)
        surf = pg.surfarray.make_surface(frame * 255)
        #applies RGB colour values to the rendered screen
        surf = pg.transform.scale(surf, (1600, 1200))
        #scale the screen to the window

        window.blit(surf, (0, 0))
        pg.display.update()
        #spawns the window somewhere on the monitor

        posX, posY, yaw, vres, halfvres, keys = movement(posX, posY, yaw, vres, halfvres, pg.key.get_pressed())
        #moves the player

def movement(posX, posY, yaw, vres, halfvres, keys):
    """fairly simple code to move the player's coordinates"""

    if keys[pg.K_LEFT] or keys[ord("a")]:
        yaw = yaw - 0.05

    if keys[pg.K_RIGHT] or keys[ord("d")]:
        yaw = yaw + 0.05

    if keys[pg.K_UP]:
        posX = posX + np.cos(yaw)*0.1
        posY = posY + np.sin(yaw)*0.1

    if keys[pg.K_DOWN]:
        posX = posX - np.cos(yaw)*0.1
        posY = posY - np.sin(yaw)*0.1

    if keys[ord("s")] and vres < halfvres*2:
        """controls the camera's  down movement by changing vertical resolution"""
        vres = vres + 10

    if keys[ord("w")] and vres > 200:
        """controls the camera's up movement by changing vertical resolution"""
        vres = vres - 10

    return posX, posY, yaw, vres, halfvres, keys

if __name__ == "__main__":
    size = 5
    num_enemies = 3
    map = create_maze(size, 'top', 'bottom', num_enemies)
    for row in map:
        print(row)

    main(map)
    pg.quit()
    #runs the game as a function instead of as hard code