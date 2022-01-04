
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
GREENDOOR = 3
YELLOWDOOR = 4
GREENKEY = 5
YELLOWKEY = 6

DOORS = [GREENDOOR, YELLOWDOOR]
ITEMS = [GREENKEY, YELLOWKEY]

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
INVENTORYSIZE = 0.8 * BLOCKSIZE;
INVENTORYMARGIN = int((BLOCKSIZE - INVENTORYSIZE) / 2)

def main():
    # file handling
    # loading initial map data from file into variables
    player = Player()

    map0 = Map("assets/map0.csv")
    map1 = Map("assets/map1.csv")

    curr_level = map1
    curr_level.load(player)
    
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

    map_assets[GREENDOOR] = pygame.image.load("assets/greendoor.png")
    map_assets[GREENDOOR] = pygame.transform.scale(map_assets[GREENDOOR], (BLOCKSIZE, BLOCKSIZE))

    map_assets[YELLOWDOOR] = pygame.image.load("assets/yellowdoor.png")
    map_assets[YELLOWDOOR] = pygame.transform.scale(map_assets[YELLOWDOOR], (BLOCKSIZE, BLOCKSIZE))

    map_assets[GREENKEY] = pygame.image.load("assets/greenkey.jpeg")
    map_assets[GREENKEY] = pygame.transform.scale(map_assets[GREENKEY], (BLOCKSIZE, BLOCKSIZE))

    map_assets[YELLOWKEY] = pygame.image.load("assets/yellowkey.jpeg")
    map_assets[YELLOWKEY] = pygame.transform.scale(map_assets[YELLOWKEY], (BLOCKSIZE, BLOCKSIZE))

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if checkNextTile(player, curr_level.map, UP):
                        player.location = player.moveUp(player.location, curr_level.map)
                elif event.key == pygame.K_a:
                    if checkNextTile(player, curr_level.map, LEFT):
                        player.location = player.moveLeft(player.location, curr_level.map)
                elif event.key == pygame.K_s:
                    if checkNextTile(player, curr_level.map, DOWN):
                        player.location = player.moveDown(player.location, curr_level.map)
                elif event.key == pygame.K_d:
                    if checkNextTile(player, curr_level.map, RIGHT):
                        player.location = player.moveRight(player.location, curr_level.map)


        # add standard game bg color
        screen.fill(BLACK)

        # find viewport bounds based on current player location and HALFVIEW
        # maintains player centered in viewport (unless edge is reached)
        col_start = player.location[0] - HALFVIEW
        row_start = player.location[1] - HALFVIEW
        if col_start < 0:
            col_start = 0
            col_end = VISIBLEBLOCKS - 1
        else:
            col_end = player.location[0] + HALFVIEW
            if col_end >= MAPWIDTH:
                col_end = MAPWIDTH - 1
                col_start = col_end - VISIBLEBLOCKS + 1

        if row_start < 0:
            row_start = 0
            row_end = VISIBLEBLOCKS - 1
        else:
            row_end = player.location[1] + HALFVIEW
            if row_end >= MAPWIDTH:
                row_end = MAPWIDTH - 1
                row_start = row_end - VISIBLEBLOCKS + 1

        # display loaded map 
        # after resolving bounds of viewport loop over currently loaded map
        # then display respective tile image from map_assets dict with screen.blit
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                screen.blit(map_assets[curr_level.map[row][col]], ((col - col_start) * BLOCKSIZE, (row - row_start) * BLOCKSIZE))

        # display UI overlay
        # inventory
        for index in range(len(player.inventory)):
            screen.blit(pygame.transform.scale(map_assets[player.inventory[index]], (INVENTORYSIZE, INVENTORYSIZE)), (index * BLOCKSIZE + INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE + INVENTORYMARGIN))

        # update display with pygame
        pygame.display.flip()


# function definitions
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

def checkNextTile(pPlayer, pMap, pDir):
    # check next location for enemies, items, etc.
    # updates map and player (inventory) accordingly
    next_tile = pMap[pPlayer.location[1] + pDir[1]][pPlayer.location[0] + pDir[0]]

    if next_tile == WALL:
        return False
    elif next_tile in DOORS:
        if next_tile == GREENDOOR and GREENKEY in pPlayer.inventory:
            pPlayer.removeItem(GREENKEY)
            print(f"inventory: {pPlayer.inventory}")
            return True
        elif next_tile == YELLOWDOOR and YELLOWKEY in pPlayer.inventory:
            pPlayer.removeItem(YELLOWKEY)
            print(f"inventory: {pPlayer.inventory}")
            return True
        else:
            return False
    elif next_tile in ITEMS:
        pPlayer.addItem(next_tile)
        print(f"inventory: {pPlayer.inventory}")
        return True
    else:
        return True


def isDanger(pLoc, pMap, pDir):
    raise NotImplementedError


# classes
class Player:
    def __init__(self):
        self.location = (0, 0)
        self.inventory = []

    def relocate(self, pLoc):
        self.location = pLoc

    def moveLeft(self, pLoc, pMap):
        new_location = (pLoc[0] - 1, pLoc[1])
        pMap[pLoc[1]][pLoc[0]] = FLOOR
        pMap[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveRight(self, pLoc, pMap):
        new_location = (pLoc[0] + 1, pLoc[1])
        pMap[pLoc[1]][pLoc[0]] = FLOOR
        pMap[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveUp(self, pLoc, pMap):
        new_location = (pLoc[0], pLoc[1] - 1)
        pMap[pLoc[1]][pLoc[0]] = FLOOR
        pMap[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveDown(self, pLoc, pMap):
        new_location = (pLoc[0], pLoc[1] + 1)
        pMap[pLoc[1]][pLoc[0]] = FLOOR
        pMap[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def addItem(self, pItem):
        self.inventory.append(pItem)

    def removeItem(self, pItem):
        self.inventory.remove(pItem)

class Map:
    def __init__(self, filepath):
        self.filepath = filepath
        self.map = []

    def load(self, player):
        map_file = open(self.filepath)
        curr_line = map_file.readline()

        player.relocate(tuple([int(x) for x in curr_line[0:-1].split(",")]))

        curr_line = map_file.readline()
        while curr_line:
            self.map.append([int(cell) for cell in curr_line[0:-1].split(",")])
            curr_line = map_file.readline()
        map_file.close()

if __name__ == "__main__":
    main()
