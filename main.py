
import sys
import pygame
import math
import random

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
THIEF = 7
EXIT = 8
CHIPDOOR = 9
CHIP = 10
NOCHIP = 11
FIRE = 12
FIMM = 13
WATER = 14
WIMM = 15
SLIDEUP = 16
SLIDEDOWN = 17
SLIDELEFT = 18
SLIDERIGHT = 19

SLIDES = [SLIDEUP, SLIDEDOWN, SLIDELEFT, SLIDERIGHT]
ELEMENTS = [FIRE, WATER]
IMMUNITY = [FIMM, WIMM]
DOORS = [GREENDOOR, YELLOWDOOR]
ITEMS = [GREENKEY, YELLOWKEY]

# DIRECTIONS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# SLIDES TO DIRECTION DICT
SDIR = {}
SDIR[SLIDEUP] = UP
SDIR[SLIDEDOWN] = DOWN
SDIR[SLIDELEFT] = LEFT
SDIR[SLIDERIGHT] = RIGHT

# SLIDES TO MOVEMENT DICT
SMOVE = {}

MAPWIDTH = 41

# making sure screen is square 1:1
SCREENWIDTH = 900
SCREENHEIGHT = SCREENWIDTH

VISIBLEBLOCKS = 9
HALFVIEW = math.floor(VISIBLEBLOCKS / 2)
BLOCKSIZE = int(SCREENWIDTH / VISIBLEBLOCKS)
INVENTORYSIZE = int(0.8 * BLOCKSIZE)
INVENTORYMARGIN = int((BLOCKSIZE - INVENTORYSIZE) / 2)

def main():
    # file handling
    # loading initial map data from file into variables
    player = Player()

    map0 = Map("map0", "assets/map0.csv")
    map1 = Map("map1", "assets/map1.csv")
    map2 = Map("map2", "assets/map2.csv")
    map3 = Map("map3", "assets/map3.csv")
    maplist = [map0, map1, map2, map3]

    # always start from start map
    mapholder = Map("holder", "")
    mapholder.swap(player, map0.name, map0.filepath)
    mapholder.load(player)
    
    # initializing SLIDES to MOVE dictionary
    SMOVE[SLIDEUP] = player.moveUp
    SMOVE[SLIDEDOWN] = player.moveDown
    SMOVE[SLIDELEFT] = player.moveLeft
    SMOVE[SLIDERIGHT] = player.moveRight

    
    # initialize pygame
    pygame.init()

    # config variables
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

    # asset variables
    # assets dict for rendering
    game_assets = {}
    game_assets[PLAYER] = pygame.image.load("assets/player.png")
    game_assets[PLAYER] = pygame.transform.scale(game_assets[PLAYER], (BLOCKSIZE, BLOCKSIZE))

    game_assets[FLOOR] = pygame.image.load("assets/floor.jpeg")
    game_assets[FLOOR] = pygame.transform.scale(game_assets[FLOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[WALL] = pygame.image.load("assets/wall.jpeg")
    game_assets[WALL] = pygame.transform.scale(game_assets[WALL], (BLOCKSIZE, BLOCKSIZE))
    game_assets[GREENDOOR] = pygame.image.load("assets/greendoor.png")
    game_assets[GREENDOOR] = pygame.transform.scale(game_assets[GREENDOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[YELLOWDOOR] = pygame.image.load("assets/yellowdoor.png")
    game_assets[YELLOWDOOR] = pygame.transform.scale(game_assets[YELLOWDOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[GREENKEY] = pygame.image.load("assets/greenkey.jpeg")
    game_assets[GREENKEY] = pygame.transform.scale(game_assets[GREENKEY], (BLOCKSIZE, BLOCKSIZE))

    game_assets[YELLOWKEY] = pygame.image.load("assets/yellowkey.jpeg")
    game_assets[YELLOWKEY] = pygame.transform.scale(game_assets[YELLOWKEY], (BLOCKSIZE, BLOCKSIZE))

    game_assets[THIEF] = pygame.image.load("assets/thief.jpeg")
    game_assets[THIEF] = pygame.transform.scale(game_assets[THIEF], (BLOCKSIZE, BLOCKSIZE))

    game_assets[EXIT] = pygame.image.load("assets/exit.png")
    game_assets[EXIT] = pygame.transform.scale(game_assets[EXIT], (BLOCKSIZE, BLOCKSIZE))

    game_assets[CHIPDOOR] = pygame.image.load("assets/chipdoor.jpeg")
    game_assets[CHIPDOOR] = pygame.transform.scale(game_assets[CHIPDOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[CHIP] = pygame.image.load("assets/chip.jpeg")
    game_assets[CHIP] = pygame.transform.scale(game_assets[CHIP], (BLOCKSIZE, BLOCKSIZE))

    game_assets[NOCHIP] = pygame.image.load("assets/nochip.png")
    game_assets[NOCHIP] = pygame.transform.scale(game_assets[NOCHIP], (BLOCKSIZE, BLOCKSIZE))

    game_assets[FIRE] = pygame.image.load("assets/fire.jpeg")
    game_assets[FIRE] = pygame.transform.scale(game_assets[FIRE], (BLOCKSIZE, BLOCKSIZE))
    game_assets[FIMM] = pygame.image.load("assets/fimm.jpeg")
    game_assets[FIMM] = pygame.transform.scale(game_assets[FIMM], (BLOCKSIZE, BLOCKSIZE))

    game_assets[WATER] = pygame.image.load("assets/water.jpeg")
    game_assets[WATER] = pygame.transform.scale(game_assets[WATER], (BLOCKSIZE, BLOCKSIZE))
    game_assets[WIMM] = pygame.image.load("assets/wimm.jpeg")
    game_assets[WIMM] = pygame.transform.scale(game_assets[WIMM], (BLOCKSIZE, BLOCKSIZE))

    game_assets[SLIDEUP] = pygame.image.load("assets/slideup.png")
    game_assets[SLIDEUP] = pygame.transform.scale(game_assets[SLIDEUP], (BLOCKSIZE, BLOCKSIZE))
    game_assets[SLIDEDOWN] = pygame.image.load("assets/slidedown.png")
    game_assets[SLIDEDOWN] = pygame.transform.scale(game_assets[SLIDEDOWN], (BLOCKSIZE, BLOCKSIZE))
    game_assets[SLIDELEFT] = pygame.image.load("assets/slideleft.png")
    game_assets[SLIDELEFT] = pygame.transform.scale(game_assets[SLIDELEFT], (BLOCKSIZE, BLOCKSIZE))
    game_assets[SLIDERIGHT] = pygame.image.load("assets/slideright.png")
    game_assets[SLIDERIGHT] = pygame.transform.scale(game_assets[SLIDERIGHT], (BLOCKSIZE, BLOCKSIZE))


    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if checkNextTile(player, mapholder, maplist, UP):
                        if (player.under in SLIDES):
                            SMOVE[player.under](player, mapholder)
                        else:
                            player.location = player.moveUp(player, mapholder)
                elif event.key == pygame.K_a:
                    if checkNextTile(player, mapholder, maplist, LEFT):
                        if (player.under in SLIDES):
                            SMOVE[player.under](player, mapholder)
                        else:
                            player.location = player.moveLeft(player, mapholder)
                elif event.key == pygame.K_s:
                    if checkNextTile(player, mapholder, maplist, DOWN):
                        if (player.under in SLIDES):
                            SMOVE[player.under](player, mapholder)
                        else:
                            player.location = player.moveDown(player, mapholder)
                elif event.key == pygame.K_d:
                    if checkNextTile(player, mapholder, maplist, RIGHT):
                        if (player.under in SLIDES):
                            SMOVE[player.under](player, mapholder)
                        else:
                            player.location = player.moveRight(player, mapholder)


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
        # then display respective tile image from game_assets dict with screen.blit
        # this only displays the tiles visible in view
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                screen.blit(game_assets[mapholder.map[row][col]], ((col - col_start) * BLOCKSIZE, (row - row_start) * BLOCKSIZE))


        # display UI overlay

        # immunity
        # bottom of screen, on top of inventory
        if player.immunity:
            screen.blit(pygame.transform.scale(game_assets[player.immunity], (INVENTORYSIZE, INVENTORYSIZE)), (INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE * 3 + INVENTORYMARGIN))

        # inventory
        # bottom of screen, on top of chips
        for index in range(len(player.inventory)):
            screen.blit(pygame.transform.scale(game_assets[player.inventory[index]], (INVENTORYSIZE, INVENTORYSIZE)), (index * BLOCKSIZE + INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE * 2 + INVENTORYMARGIN))

        # chips
        # bottom of screen 
        for index in range(mapholder.chips):
            if index < player.chips:
                icon = game_assets[CHIP]
            else:
                icon = game_assets[NOCHIP]
            screen.blit(pygame.transform.scale(icon, (INVENTORYSIZE, INVENTORYSIZE)), (index * BLOCKSIZE + INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE + INVENTORYMARGIN))

        # update display with pygame
        pygame.display.flip()




def checkNextTile(pPlayer, pMap, pMapList, pDir):
    # check next location for enemies, items, etc.
    # updates map and player (inventory) accordingly
    next_tile = pMap.map[pPlayer.location[1] + pDir[1]][pPlayer.location[0] + pDir[0]]

    if next_tile == WALL:
        return False
    elif next_tile in DOORS:
        if next_tile == GREENDOOR and GREENKEY in pPlayer.inventory:
            pPlayer.removeItem(GREENKEY)
            return True
        elif next_tile == YELLOWDOOR and YELLOWKEY in pPlayer.inventory:
            pPlayer.removeItem(YELLOWKEY)
            return True
        else:
            return False
    elif next_tile in ITEMS:
        pPlayer.addItem(next_tile)
        return True
    elif next_tile in IMMUNITY:
        pPlayer.immunity = next_tile
        return True
    elif next_tile in ELEMENTS:
        if next_tile == FIRE and pPlayer.immunity == FIMM:
            return True
        elif next_tile == WATER and pPlayer.immunity == WIMM:
            return True
        else:
            lose()
    elif next_tile == THIEF:
        restartLevel(pPlayer, pMap)
        return True
    elif next_tile == EXIT:
        win(pPlayer, pMap, pMapList)
        return True
    elif next_tile == CHIP:
        pPlayer.addChip()
        return True
    elif next_tile == CHIPDOOR:
        if pMap.chips == pPlayer.chips:
            return True
        else:
            return False
    elif next_tile in SLIDES:
        if pDir == UP:
            pPlayer.relocate(pPlayer.moveUp(pPlayer, pMap))
        elif pDir == DOWN:
            pPlayer.relocate(pPlayer.moveDown(pPlayer, pMap))
        elif pDir == LEFT:
            pPlayer.relocate(pPlayer.moveLeft(pPlayer, pMap))
        else:
            pPlayer.relocate(pPlayer.moveRight(pPlayer, pMap))

        return checkNextTile(pPlayer, pMap, pMapList, SDIR[next_tile])
    else:
        return True

def restartLevel(pPlayer, pMap):
    pPlayer.clearInventory()
    pPlayer.clearImmunity()
    pPlayer.clearChips()
    pMap.load(pPlayer)

def lose():
    # temporary lost
    print("You lost!")
    sys.exit()

def win(pPlayer, pMap, pMapList):
    # remove current map from map list
    index = 0
    for m in range(len(pMapList)):
        if pMap.name == pMapList[m].name:
            index = m
    print(f"You cleared {pMapList[index].name}");
    del pMapList[index]

    # temporary win
    if not pMapList:
        print("You win! All levels done!")
        sys.exit()
    else:
        # randomly choose from available maps
        choice = random.choice(pMapList)
        pMap.swap(pPlayer, choice.name, choice.filepath)
        restartLevel(pPlayer, pMap)


# classes
class Player:
    def __init__(self):
        self.location = (0, 0)
        self.chips = 0
        self.immunity = 0
        self.under = 0
        self.inventory = []

    def relocate(self, pLoc):
        self.location = pLoc

    def moveLeft(self, pPlayer, pMap):
        new_location = (pPlayer.location[0] - 1, pPlayer.location[1])

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = FLOOR
        else:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = pPlayer.under

        pPlayer.under = pMap.map[new_location[1]][new_location[0]]
        pPlayer.relocate(new_location)

        pMap.map[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveRight(self, pPlayer, pMap):
        new_location = (pPlayer.location[0] + 1, pPlayer.location[1])

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = FLOOR
        else:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = pPlayer.under

        pPlayer.under = pMap.map[new_location[1]][new_location[0]]
        pPlayer.relocate(new_location)

        pMap.map[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveUp(self, pPlayer, pMap):
        new_location = (pPlayer.location[0], pPlayer.location[1] - 1)

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = FLOOR
        else:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = pPlayer.under

        pPlayer.under = pMap.map[new_location[1]][new_location[0]]
        pPlayer.relocate(new_location)

        pMap.map[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveDown(self, pPlayer, pMap):
        new_location = (pPlayer.location[0], pPlayer.location[1] + 1)

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = FLOOR
        else:
            pMap.map[pPlayer.location[1]][pPlayer.location[0]] = pPlayer.under

        pPlayer.under = pMap.map[new_location[1]][new_location[0]]
        pPlayer.relocate(new_location)

        pMap.map[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def clearInventory(self):
        self.inventory = []

    def clearImmunity(self):
        self.immunity = 0

    def clearChips(self):
        self.chips = 0

    def addChip(self):
        self.chips += 1

    def addItem(self, pItem):
        self.inventory.append(pItem)

    def removeItem(self, pItem):
        self.inventory.remove(pItem)

class Map:
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.chips = 0
        self.map = []

    def load(self, player):
        self.map = []
        map_file = open(self.filepath)

        curr_line = map_file.readline()
        self.chips = int(curr_line[:-1])

        curr_line = map_file.readline()
        player.relocate(tuple([int(x) for x in curr_line[0:-1].split(",")]))
        player.under = 0

        curr_line = map_file.readline()
        while curr_line:
            self.map.append([int(cell) for cell in curr_line[0:-1].split(",")])
            curr_line = map_file.readline()
        map_file.close()

    def swap(self, pPlayer, name, filepath):
        self.name = name
        self.filepath = filepath
        self.load(pPlayer)

if __name__ == "__main__":
    main()
