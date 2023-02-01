# OutBack(rooms)
# Alpha, Gec master and nyaw ‹𝟹
# (Aaron and Lucas)
# PYGAME AND NUMPY REQUIRED, MATH CAN REPLACE NUMPY MAYBE WITH SMALL MODIFICATIONS BUT I DON'T WANT TO BOTHER
import pygame as pg
import numpy as np
# import numba

import random


# Creating player
class Player:
    # Creation code
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Creating enemy
class Enemy:
    # Creation code
    def __init__(self, x, y):
        self.x = x
        self.y = y


class DisjointSet:
    """For the creation of a randgen map"""

    def __init__(self, n):
        # Initialize the number of elements
        self.n = n
        # Create a list to store the parents of each element
        self.parents = list(range(n))
        # Create a list to store the rank of each element
        self.ranks = [0] * n

    def find(self, x):
        # Find the representative element (root) of the set that contains x
        # Check if the element is not already the root

        if self.parents[x] != x:
            # Path compression: set the parent of x to the root of its set
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        # Merge the sets that contain x and y
        # Find the roots of the sets that contain x and y
        x_root, y_root = self.find(x), self.find(y)
        # Return if the elements are already in the same set

        if x_root == y_root:
            return
        # Use union by rank: attach the smaller tree to the root of the larger tree

        if self.ranks[x_root] < self.ranks[y_root]:
            x_root, y_root = y_root, x_root
        self.parents[y_root] = x_root
        # Increase the rank of the new root if both trees have the same rank

        if self.ranks[x_root] == self.ranks[y_root]:
            self.ranks[x_root] += 1


def make_maze(w, h, wall_percentage):
    """Generates a random map within set params"""
    # Initialize the grid with all walls
    grid = [[1 for x in range(w)] for y in range(h)]
    # Create a disjoint set data structure to keep track of connected cells
    sets = DisjointSet(w * h)
    # Create a list of all walls in the grid
    walls = []

    for x in range(w):
        for y in range(h):
            if x < w - 1:
                walls.append((x, y, x + 1, y))
            if y < h - 1:
                walls.append((x, y, x, y + 1))
    # Shuffle the wall list to ensure a random order
    random.shuffle(walls)
    # Number of walls to keep
    num_walls = int(len(walls) * wall_percentage)
    # Iterate through the wall list and remove walls between cells in different sets

    for wall in walls[:num_walls]:
        x1, y1, x2, y2 = wall
        if sets.find(y1 * w + x1) != sets.find(y2 * w + x2):
            sets.union(y1 * w + x1, y2 * w + x2)
            # remove walls between cells in different sets
            if x1 == x2:
                grid[min(y1, y2)][x1] = 0
            else:
                grid[y1][min(x1, x2)] = 0

    # DFS algorithm to find the path from one end of the grid to the other
    stack = [(0, 0)]
    visited = set()

    while stack:
        x, y = stack.pop()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if 0 <= x + dx < w and 0 <= y + dy < h and grid[y + dy][x + dx] == 0:
                stack.append((x + dx, y + dy))
    # Remove any walls that are not part of the path

    for y in range(h):
        for x in range(w):
            if (x, y) not in visited:
                grid[y][x] = 1
    return grid


# TODO: FIX WALLS
def main(map):
    """Main function, operating to render a screen and take basic game data"""
    pg.init()
    window = pg.display.set_mode((1600, 1200))
    running = True
    clock = pg.time.Clock()
    hres = 360  # horizontal resolution, must be a multiple of 120
    halfvres = 200  # half of the vertical resolution, must be a multiple of 100 that is divisible by hres
    vres = 300  # actual full vertical resolution
    fov = 50
    # ackshually it's both fov and camera height
    mod = hres / fov
    # pixels per degree, horizontal
    posX = 0
    posY = 0
    # player coords
    yaw = 0
    # player angle deviation from 0
    frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))
    # textureless texture, randomely generated
    fps = int(clock.get_fps())
    floor = pg.surfarray.array3d(pg.image.load('floor.jpg')) / 255
    wall = pg.surfarray.array3d(pg.image.load('wall.jpg')) / 255
    # loads images from the project folder

    while running:
        for event in pg.event.get():

            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
                # runs the game

        for i in range(hres):
            """get every column of pixels between -fov/2 and +fov/2"""
            columnAngle = yaw + np.deg2rad(i / mod - (fov / 2))
            sin = np.sin(columnAngle)
            cos = np.cos(columnAngle)
            # gets the location coordinate of this particular column
            adjustCos = np.cos(np.deg2rad(i / mod - (fov / 2)))
            # variable to prevent warping
            # frame[i][:] == floor[int(np.rad2deg(columnAngle)%99)][:]

            for p in reversed(range(halfvres, halfvres*2)):
                """renders ceiling(nonfunctional)"""
                n = ((halfvres*2) / (halfvres*2 - p)) / adjustCos
                # determines the distance from the player's coordinates to the target pixel
                pixelX = posX + cos * n
                pixelY = posY + sin * n
                # determines the location of said pixel in the camera in relation to the player location
                amendedX = int(pixelX * 2 % 1 * 99)
                amendedY = int(pixelY * 2 % 1 * 99)
                # converts pixel coordinates to int such that it can be found on the textures
                shade = 0.1 - 0.1 * (1 - p / halfvres)

                frame[i][halfvres * 2 - p - 1] = shade * floor[amendedX][amendedY]

            for p in range(halfvres):
                """for every column of pixels, find the colour of each pixel in said column from the bottom up"""
                n = ((halfvres) / (halfvres - p)) / adjustCos
                # determines the distance from the player's coordinates to the target pixel
                pixelX = posX + cos * n
                pixelY = posY + sin * n
                # determines the location of said pixel in the camera in relation to the player location
                amendedX = int(pixelX * 2 % 1 * 99)
                amendedY = int(pixelY * 2 % 1 * 99)
                # converts pixel coordinates to int such that it can be found on the textures
                shade = 0.1 + 0.1 * (1 - p / halfvres*2)
                # light strength plus max brightness value times the base floor pixel colour

                if map[int(pixelX) % len(map)][int(pixelY % len(map))] == 1:
                    wallheight = halfvres - p
                    paint = shade * np.ones(3)

                    for k in range(wallheight * 2):
                        frame[i][halfvres - wallheight + k] = paint
                    break

                else:
                    frame[i][halfvres * 2 - p - 1] = shade * floor[amendedX][amendedY]
                    # renders the pixel at the right colour
                    # halfvres*2 = render all the way up to the top of the screen

        #        frame = new_frame(posX, posY, rot, frame, hres, halfvres, mod)
        surf = pg.surfarray.make_surface(frame * 255)
        # applies RGB colour values to the rendered screen
        surf = pg.transform.scale(surf, (1600, 1200))
        # scale the screen to the window
        window.blit(surf, (0, 0))
        pg.display.update()
        empty = pg.Color(0, 0, 0, 0)
        surf.fill(empty)
        # spawns the window somewhere on the monitor
        posX, posY, yaw, vres, halfvres, keys = movement(posX, posY, yaw, vres, halfvres, pg.key.get_pressed())
        # moves the player


def movement(posX, posY, yaw, vres, halfvres, keys):
    """fairly simple code to move the player's coordinates"""

    if keys[pg.K_LEFT] or keys[ord("a")]:
        yaw = yaw - 0.05

    if keys[pg.K_RIGHT] or keys[ord("d")]:
        yaw = yaw + 0.05

    if keys[pg.K_UP] or keys[ord("w")]:
        posX = posX + np.cos(yaw) * 0.1
        posY = posY + np.sin(yaw) * 0.1

    if keys[pg.K_DOWN] or keys[ord("s")]:
        posX = posX - np.cos(yaw) * 0.1
        posY = posY - np.sin(yaw) * 0.1

    return posX, posY, yaw, vres, halfvres, keys


if __name__ == "__main__":
    size = 20
    num_enemies = 3
    map = make_maze(size, size, 20)

    for row in map:
        print(row)
    main(map)
    pg.quit()
    # runs the game as a function instead of as hard code
