
import sys
import pygame
import math

# constants

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# symbols
FLOOR = 0
WALL = 1
PLAYER = 2
DOOR = 3
IMPASSABLE = [WALL, DOOR]

# DIRECTIONS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

MAPWIDTH = 41

# making sure screen is square 1:1
SCREENWIDTH = 900
SCREENHEIGHT = SCREENWIDTH

VISIBLEBLOCKS = 9
HALFVIEW = math.floor(VISIBLEBLOCKS / 2)
BLOCKSIZE = SCREENWIDTH / VISIBLEBLOCKS

def main():
    # file handling
    # loading initial map data from file into variables
    map_file = open("assets/map1.csv")

    curr_line = map_file.readline()
    player_location = tuple([int(x) for x in curr_line[0:-1].split(",")])

    curr_map = []
    
    curr_line = map_file.readline()
    while curr_line:
        curr_map.append([int(cell) for cell in curr_line[0:-1].split(",")])
        curr_line = map_file.readline()

    # initialize pygame
    pygame.init()

    # config variables
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

    # asset variables

    # asset dict for map rendering
    map_assets = {}

    map_assets[PLAYER] = pygame.image.load("assets/player.png")
    map_assets[PLAYER] = pygame.transform.scale(map_assets[PLAYER], (BLOCKSIZE, BLOCKSIZE))

    map_assets[FLOOR] = pygame.image.load("assets/floor.jpeg")
    map_assets[FLOOR] = pygame.transform.scale(map_assets[FLOOR], (BLOCKSIZE, BLOCKSIZE))

    map_assets[WALL] = pygame.image.load("assets/wall.jpeg")
    map_assets[WALL] = pygame.transform.scale(map_assets[WALL], (BLOCKSIZE, BLOCKSIZE))

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if isPassable(player_location, curr_map, UP):
                        player_location = playerMoveUp(player_location, curr_map)
                elif event.key == pygame.K_a:
                    if isPassable(player_location, curr_map, LEFT):
                        player_location = playerMoveLeft(player_location, curr_map)
                elif event.key == pygame.K_s:
                    if isPassable(player_location, curr_map, DOWN):
                        player_location = playerMoveDown(player_location, curr_map)
                elif event.key == pygame.K_d:
                    if isPassable(player_location, curr_map, RIGHT):
                        player_location = playerMoveRight(player_location, curr_map)

        # add standard game bg color
        screen.fill(BLACK)

        # find viewport bounds based on current player location and HALFVIEW
        # maintains player centered in viewport (unless edge is reached)
        col_start = player_location[0] - HALFVIEW
        row_start = player_location[1] - HALFVIEW
        if col_start < 0:
            col_start = 0
            col_end = VISIBLEBLOCKS - 1
        else:
            col_end = player_location[0] + HALFVIEW
            if col_end >= MAPWIDTH:
                col_end = MAPWIDTH - 1
                col_start = col_end - VISIBLEBLOCKS + 1

        if row_start < 0:
            row_start = 0
            row_end = VISIBLEBLOCKS - 1
        else:
            row_end = player_location[1] + HALFVIEW
            if row_end >= MAPWIDTH:
                row_end = MAPWIDTH - 1
                row_start = row_end - VISIBLEBLOCKS + 1

        # display loaded map 
        # after resolving bounds of viewport loop over currently loaded map
        # then display respective tile image from map_assets dict with screen.blit
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                screen.blit(map_assets[curr_map[row][col]], ((col - col_start) * BLOCKSIZE, (row - row_start) * BLOCKSIZE))

        # update display with pygame
        pygame.display.flip()


def printMap(pMap):
    '''
    hatdog
    '''
    print(f"{len(pMap)} rows")
    print(f"{len(pMap[0])} cols")
    for row in pMap:
        for col in row:
            print(f"{col}", end="")
        print()

def isPassable(pLoc, pMap, pDir):
    return not (pMap[pLoc[1] + pDir[1]][pLoc[0] + pDir[0]] in IMPASSABLE)

def isDanger(pLoc, pMap, pDir):
    raise NotImplementedError

def playerMoveLeft(pLoc, pMap):
    new_location = (pLoc[0] - 1, pLoc[1])
    pMap[pLoc[1]][pLoc[0]] = FLOOR
    pMap[new_location[1]][new_location[0]] = PLAYER
    return new_location

def playerMoveRight(pLoc, pMap):
    new_location = (pLoc[0] + 1, pLoc[1])
    pMap[pLoc[1]][pLoc[0]] = FLOOR
    pMap[new_location[1]][new_location[0]] = PLAYER
    return new_location

def playerMoveUp(pLoc, pMap):
    new_location = (pLoc[0], pLoc[1] - 1)
    pMap[pLoc[1]][pLoc[0]] = FLOOR
    pMap[new_location[1]][new_location[0]] = PLAYER
    return new_location

def playerMoveDown(pLoc, pMap):
    new_location = (pLoc[0], pLoc[1] + 1)
    pMap[pLoc[1]][pLoc[0]] = FLOOR
    pMap[new_location[1]][new_location[0]] = PLAYER
    return new_location

def displayMap(pMap):
    raise NotImplementedError

if __name__ == "__main__":
    main()
