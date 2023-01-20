#OutBack(rooms)
#Alpha, Gec master and nyaw ‹𝟹
#(Aaron and Lucas)

import pygame as pg
import numpy as np


#TODO: ADD A WAY TO MOVE THE CAMERA UP AND DOWN
def main():
    pg.init()
    window = pg.display.set_mode((800, 600))
    running = True
#    clock = pg.time.Clock()

    hres = 360#horizontal resolution, must be a multiple of 120
    halfvres = 200#half of the vertical resolution, must be a multiple of 100 that is divisible by hres
    fov = 20
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
    #loads images from the project folder

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

            for p in range(halfvres):
                """for every column of pixels, find the colour of each pixel in said column from the bottom up"""
                n = (halfvres/(halfvres-p))/adjustCos
                #determines the distance from the player's coordinates to the target pixel
                pixelX = posX + cos*n
                pixelY = posY + sin*n
                #determines the location of said pixel in the camera in relation to the player location

                amendedX = int(pixelX * 2 % 1 * 99)
                amendedY = int(pixelY * 2 % 1 * 99)
                #converts pixel coordinates to int such that it can be found on the textures

                shade = 0.2 + 0.3 * (1 - p / halfvres)
                #light strength plus max brightness value times the base floor pixel colour

                frame[i][halfvres * 2 - p - 1] = shade*floor[amendedX][amendedY]
                #renders the pixel at the right colour

#        frame = new_frame(posX, posY, rot, frame, hres, halfvres, mod)
        surf = pg.surfarray.make_surface(frame * 255)
        #applies RGB colour values to the rendered screen
        surf = pg.transform.scale(surf, (800, 600))
        #scale the screen to the window

        window.blit(surf, (0, 0))
        pg.display.update()
        #spawns the window somewhere on the monitor

        posX, posY, yaw, keys = movement(posX, posY, yaw, pg.key.get_pressed())
        #moves the player


def movement(posX, posY, yaw, keys):
    """fairly simple code to move the player's coordinates"""

    if keys[pg.K_LEFT] or keys[ord("a")]:
        yaw = yaw - 0.05

    if keys[pg.K_RIGHT] or keys[ord("d")]:
        yaw = yaw + 0.05

    if keys[pg.K_UP] or keys[ord("w")]:
        posX = posX + np.cos(yaw)*0.1
        posY = posY + np.sin(yaw)*0.1

    if keys[pg.K_DOWN] or keys[ord("s")]:
        posX = posX - np.cos(yaw)*0.1
        posY = posY - np.sin(yaw)*0.1

    return posX, posY, yaw, keys

if __name__ == "__main__":
    main()
    pg.quit()
    #runs the game as a function instead of as hard code