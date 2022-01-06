
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
GREENKEYTILE = 5
YELLOWKEYTILE = 6
THIEF = 7
EXIT = 8
CHIPDOOR = 9
CHIPTILE = 10
NOCHIP = 11
FIRE = 12
FIMMTILE = 13
WATER = 14
WIMMTILE = 15
SLIDEUP = 16
SLIDEDOWN = 17
SLIDELEFT = 18
SLIDERIGHT = 19
CHIP = 20
FIMM = 21
WIMM = 22
PLAYERMAP = 23
PLAYERUP = 24
PLAYERLEFT = 25
PLAYERRIGHT = 26
GREENKEY = 27
YELLOWKEY = 28

SLIDES = [SLIDEUP, SLIDEDOWN, SLIDELEFT, SLIDERIGHT]
ELEMENTS = [FIRE, WATER]
IMMUNITY = [FIMMTILE, WIMMTILE]
DOORS = [GREENDOOR, YELLOWDOOR, CHIPDOOR]
ITEMS = [GREENKEYTILE, YELLOWKEYTILE]

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
SPRITESIZE = 20
INVENTORYSIZE = int(0.8 * BLOCKSIZE)
INVENTORYMARGIN = int((BLOCKSIZE - INVENTORYSIZE) / 2)
INVENTORYTILT = 20

MAPOFFSET = int((SCREENWIDTH - MAPWIDTH * SPRITESIZE) / 2)

def main():
    # initializations
    overlay = Overlay()
    mapOverlay = False

    # file handling
    # loading initial map data from file into variables
    player = Player()

    map0 = Map("map0", "assets/map0.csv")
    map1 = Map("map1", "assets/map1.csv")
    map2 = Map("map2", "assets/map2.csv")
    map3 = Map("map3", "assets/map3.csv")

    allmaps = [map0, map1, map2, map3]
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

    # fonts
    overlayFont = pygame.font.Font("assets/8bit.ttf", 12)

    # assets dict for rendering
    game_assets = {}
    game_assets[PLAYER] = pygame.image.load("assets/playerdown.png")
    game_assets[PLAYER] = pygame.transform.scale(game_assets[PLAYER], (BLOCKSIZE, BLOCKSIZE))
    game_assets[PLAYERLEFT] = pygame.image.load("assets/playerleft.png")
    game_assets[PLAYERLEFT] = pygame.transform.scale(game_assets[PLAYERLEFT], (BLOCKSIZE, BLOCKSIZE))

    game_assets[PLAYERRIGHT] = pygame.image.load("assets/playerright.png")
    game_assets[PLAYERRIGHT] = pygame.transform.scale(game_assets[PLAYERRIGHT], (BLOCKSIZE, BLOCKSIZE))

    game_assets[PLAYERUP] = pygame.image.load("assets/playerup.png")
    game_assets[PLAYERUP] = pygame.transform.scale(game_assets[PLAYERUP], (BLOCKSIZE, BLOCKSIZE))

    game_assets[PLAYERMAP] = pygame.image.load("assets/playermap.png")
    game_assets[PLAYERMAP] = pygame.transform.scale(game_assets[PLAYERMAP], (BLOCKSIZE, BLOCKSIZE))

    game_assets[FLOOR] = pygame.image.load("assets/floor.png")
    game_assets[FLOOR] = pygame.transform.scale(game_assets[FLOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[WALL] = pygame.image.load("assets/wall.png")
    game_assets[WALL] = pygame.transform.scale(game_assets[WALL], (BLOCKSIZE, BLOCKSIZE))
    game_assets[GREENDOOR] = pygame.image.load("assets/greendoor.png")
    game_assets[GREENDOOR] = pygame.transform.scale(game_assets[GREENDOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[YELLOWDOOR] = pygame.image.load("assets/yellowdoor.png")
    game_assets[YELLOWDOOR] = pygame.transform.scale(game_assets[YELLOWDOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[GREENKEYTILE] = pygame.image.load("assets/greenkeytile.png")
    game_assets[GREENKEYTILE] = pygame.transform.scale(game_assets[GREENKEYTILE], (BLOCKSIZE, BLOCKSIZE))

    game_assets[YELLOWKEYTILE] = pygame.image.load("assets/yellowkeytile.png")
    game_assets[YELLOWKEYTILE] = pygame.transform.scale(game_assets[YELLOWKEYTILE], (BLOCKSIZE, BLOCKSIZE))

    game_assets[GREENKEY] = pygame.image.load("assets/greenkey.png")
    game_assets[GREENKEY] = pygame.transform.scale(game_assets[GREENKEY], (BLOCKSIZE, BLOCKSIZE))

    game_assets[YELLOWKEY] = pygame.image.load("assets/yellowkey.png")
    game_assets[YELLOWKEY] = pygame.transform.scale(game_assets[YELLOWKEY], (BLOCKSIZE, BLOCKSIZE))

    game_assets[THIEF] = pygame.image.load("assets/thief.png")
    game_assets[THIEF] = pygame.transform.scale(game_assets[THIEF], (BLOCKSIZE, BLOCKSIZE))

    game_assets[EXIT] = pygame.image.load("assets/exit.png")
    game_assets[EXIT] = pygame.transform.scale(game_assets[EXIT], (BLOCKSIZE, BLOCKSIZE))

    game_assets[CHIPDOOR] = pygame.image.load("assets/chipdoor.png")
    game_assets[CHIPDOOR] = pygame.transform.scale(game_assets[CHIPDOOR], (BLOCKSIZE, BLOCKSIZE))

    game_assets[CHIP] = pygame.image.load("assets/chip.png")
    game_assets[CHIP] = pygame.transform.scale(game_assets[CHIP], (BLOCKSIZE, BLOCKSIZE))

    game_assets[CHIPTILE] = pygame.image.load("assets/chiptile.png")
    game_assets[CHIPTILE] = pygame.transform.scale(game_assets[CHIPTILE], (BLOCKSIZE, BLOCKSIZE))

    game_assets[NOCHIP] = pygame.image.load("assets/nochip.png")
    game_assets[NOCHIP] = pygame.transform.scale(game_assets[NOCHIP], (BLOCKSIZE, BLOCKSIZE))

    game_assets[FIRE] = pygame.image.load("assets/fire.png")
    game_assets[FIRE] = pygame.transform.scale(game_assets[FIRE], (BLOCKSIZE, BLOCKSIZE))
    game_assets[FIMMTILE] = pygame.image.load("assets/fimmtile.png")
    game_assets[FIMMTILE] = pygame.transform.scale(game_assets[FIMMTILE], (BLOCKSIZE, BLOCKSIZE))

    game_assets[FIMM] = pygame.image.load("assets/fimm.png")
    game_assets[FIMM] = pygame.transform.scale(game_assets[FIMM], (BLOCKSIZE, BLOCKSIZE))

    game_assets[WATER] = pygame.image.load("assets/water.png")
    game_assets[WATER] = pygame.transform.scale(game_assets[WATER], (BLOCKSIZE, BLOCKSIZE))
    game_assets[WIMMTILE] = pygame.image.load("assets/wimmtile.png")
    game_assets[WIMMTILE] = pygame.transform.scale(game_assets[WIMMTILE], (BLOCKSIZE, BLOCKSIZE))

    game_assets[WIMM] = pygame.image.load("assets/wimm.png")
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
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                sys.exit()
            elif event.type == pygame.KEYDOWN and not overlay.isVisible():
                if event.key == pygame.K_w:
                    if checkNextTile(player, mapholder, maplist, UP, overlay):
                        if (player.under in SLIDES):
                            SMOVE[player.under](mapholder)
                        else:
                            player.relocate(player.moveUp(mapholder))
                elif event.key == pygame.K_a:
                    if checkNextTile(player, mapholder, maplist, LEFT, overlay):
                        if (player.under in SLIDES):
                            SMOVE[player.under](mapholder)
                        else:
                            player.relocate(player.moveLeft(mapholder))
                elif event.key == pygame.K_s:
                    if checkNextTile(player, mapholder, maplist, DOWN, overlay):
                        if (player.under in SLIDES):
                            SMOVE[player.under](mapholder)
                        else:
                            player.relocate(player.moveDown(mapholder))
                elif event.key == pygame.K_d:
                    if checkNextTile(player, mapholder, maplist, RIGHT, overlay):
                        if (player.under in SLIDES):
                            SMOVE[player.under](mapholder)
                        else:
                            player.relocate(player.moveRight(mapholder))
                elif event.key == pygame.K_m:
                    mapOverlay = True
                    overlay.showOverlay()
                elif event.key == pygame.K_r:
                    restartLevel(player, mapholder, overlay)
                elif event.key == pygame.K_ESCAPE:
                    restartMapList(allmaps, maplist)
                    restartGame(player, mapholder, map0, overlay)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restartLevel(player, mapholder, overlay)
                elif event.key == pygame.K_ESCAPE:
                    restartGame(player, mapholder, map0, overlay)
                elif event.key == pygame.K_SPACE and player.clear:
                    player.clear = False
                    overlay.hideOverlay()
                    nextLevel(player, mapholder, maplist, overlay)
            elif event.type == pygame.KEYUP and mapOverlay:
                if event.key == pygame.K_m:
                    mapOverlay = False
                    overlay.hideOverlay()

        # add standard game bg color
        screen.fill(BLACK)

        if not overlay.isVisible():
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
                    if (col, row) == player.location:
                        if player.under in ITEMS or player.under in IMMUNITY or player.under in DOORS:
                            # if under player is item, render floor
                            screen.blit(game_assets[FLOOR], ((col - col_start) * BLOCKSIZE, (row - row_start) * BLOCKSIZE))
                        else:
                            # else render whatever is under
                            screen.blit(game_assets[player.under], ((col - col_start) * BLOCKSIZE, (row - row_start) * BLOCKSIZE))

                        # displays player sprite on top of tile
                        if player.orientation == DOWN:
                            player_sprite = game_assets[PLAYER]
                        elif player.orientation == LEFT:
                            player_sprite = game_assets[PLAYERLEFT]
                        elif player.orientation == UP:
                            player_sprite = game_assets[PLAYERUP]
                        else:
                            player_sprite = game_assets[PLAYERRIGHT]

                        screen.blit(player_sprite, ((col - col_start) * BLOCKSIZE, (row - row_start) * BLOCKSIZE))
                    else:
                        # displays map tile
                        screen.blit(game_assets[mapholder.map[row][col]], ((col - col_start) * BLOCKSIZE, (row - row_start) * BLOCKSIZE))


            # display UI overlay

            # immunity
            # bottom of screen, on top of inventory
            if player.immunity:
                screen.blit(pygame.transform.scale(pygame.transform.rotate(game_assets[player.immunity], INVENTORYTILT), (INVENTORYSIZE, INVENTORYSIZE)), (INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE * 3))

            # inventory
            # bottom of screen, on top of chips
            for index in range(len(player.inventory)):
                screen.blit(pygame.transform.scale(pygame.transform.rotate(game_assets[player.inventory[index]], INVENTORYTILT), (INVENTORYSIZE, INVENTORYSIZE)), (index * INVENTORYSIZE + INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE * 2))

            # chips
            # bottom of screen 
            for index in range(mapholder.chips):
                if index < player.chips:
                    icon = game_assets[CHIP]
                else:
                    icon = game_assets[NOCHIP]

                screen.blit(pygame.transform.scale(pygame.transform.rotate(icon, INVENTORYTILT), (INVENTORYSIZE, INVENTORYSIZE)), (index * INVENTORYSIZE + INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE))

            # UI text
            uiText = overlayFont.render("Immunity", False, WHITE)
            screen.blit(uiText, (INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE * 3 - INVENTORYMARGIN))
            uiText = overlayFont.render("Inventory", False, WHITE)
            screen.blit(uiText, (INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE * 2 - INVENTORYMARGIN))

            uiText = overlayFont.render("Chips", False, WHITE)
            screen.blit(uiText, (INVENTORYMARGIN, SCREENHEIGHT - BLOCKSIZE * 1 - INVENTORYMARGIN))
        else:
            if not mapOverlay:
                # display normal message overlay
                screen.fill(BLACK)
                overlayText = overlayFont.render(overlay.message, False, WHITE)
                overlayTextRect = overlayText.get_rect()
                overlayTextRect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)
                screen.blit(overlayText, overlayTextRect)
            else:
                # display map
                for row in range(len(mapholder.map)):
                    for col in range(len(mapholder.map[0])):
                        if (col, row) == player.location:
                            screen.blit(pygame.transform.scale(game_assets[PLAYERMAP], (SPRITESIZE, SPRITESIZE)), (MAPOFFSET + col * SPRITESIZE,MAPOFFSET + row * SPRITESIZE))
                        else:
                            screen.blit(pygame.transform.scale(game_assets[mapholder.map[row][col]], (SPRITESIZE, SPRITESIZE)), (MAPOFFSET + col * SPRITESIZE, MAPOFFSET + row * SPRITESIZE))
        
        # display controls
        controlsText = overlayFont.render("[ M ] Map    [ R ] Restart Level    [ ESC ] Restart Game", False, WHITE)
        controlsTextRect = controlsText.get_rect()
        controlsTextRect.center = (SCREENWIDTH // 2, BLOCKSIZE // 2)
        screen.blit(controlsText, controlsTextRect)

        # update display with pygame
        pygame.display.flip()

def checkNextTile(pPlayer, pMap, pMapList, pDir, pOverlay):
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
        elif next_tile == CHIPDOOR:
            if pMap.chips == pPlayer.chips:
                return True

        return False
    elif next_tile in ITEMS:
        if next_tile == GREENKEYTILE: pPlayer.addItem(GREENKEY)
        elif next_tile == YELLOWKEYTILE:
            pPlayer.addItem(YELLOWKEY)
        return True
    elif next_tile in IMMUNITY:
        if next_tile == FIMMTILE:
            pPlayer.immunity = FIMM
        else:
            pPlayer.immunity = WIMM
        return True
    elif next_tile in ELEMENTS:
        if next_tile == FIRE and pPlayer.immunity == FIMM:
            return True
        elif next_tile == WATER and pPlayer.immunity == WIMM:
            return True
        else:
            lose(pOverlay)
    elif next_tile == THIEF:
        restartLevel(pPlayer, pMap, pOverlay)
        return True
    elif next_tile == EXIT:
        win(pPlayer, pMap, pMapList, pOverlay)
        return False
    elif next_tile == CHIPTILE:
        pPlayer.addChip()
        return True
    elif next_tile in SLIDES:
        if pDir == UP:
            pPlayer.relocate(pPlayer.moveUp(pMap))
        elif pDir == DOWN:
            pPlayer.relocate(pPlayer.moveDown(pMap))
        elif pDir == LEFT:
            pPlayer.relocate(pPlayer.moveLeft(pMap))
        else:
            pPlayer.relocate(pPlayer.moveRight(pMap))

        return checkNextTile(pPlayer, pMap, pMapList, SDIR[next_tile], pOverlay)
    else:
        return True

def restartLevel(pPlayer, pMap, pOverlay):
    pOverlay.hideOverlay()
    pPlayer.clearInventory()
    pPlayer.clearImmunity()
    pPlayer.clearChips()
    pMap.load(pPlayer)

def restartMapList(pAllMaps, pMapList):
    pMapList.clear()
    for m in pAllMaps:
        pMapList.append(m)

def restartGame(pPlayer, pMap, pStartMap, pOverlay):
    pOverlay.hideOverlay()
    pMap.swap(pPlayer, pStartMap.name, pStartMap.filepath)
    restartLevel(pPlayer, pMap, pOverlay)

def nextLevel(pPlayer, pMap, pMapList, pOverlay):
    # remove current map from map list
    index = 0
    for m in range(len(pMapList)):
        if pMap.name == pMapList[m].name:
            index = m
    del pMapList[index]

    # randomly choose from available maps
    choice = random.choice(pMapList)
    pMap.swap(pPlayer, choice.name, choice.filepath)
    restartLevel(pPlayer, pMap, pOverlay)

def lose(pOverlay):
    # display lost in overlay
    pOverlay.showOverlay()
    pOverlay.changeMessage("You lost!")

def win(pPlayer, pMap, pMapList, pOverlay):
    # display win in overlay
    if not pMapList:
        pOverlay.showOverlay()
        pOverlay.changeMessage("You won! All levels completed!")
    else:
        pPlayer.clear = True
        pOverlay.showOverlay()
        pOverlay.changeMessage("Map cleared! Press SPACE to continue")


# classes
class Player:
    def __init__(self):
        self.orientation = DOWN
        self.clear = False
        self.location = (0, 0)
        self.chips = 0
        self.immunity = 0
        self.under = 0
        self.inventory = []

    def relocate(self, pLoc):
        self.location = pLoc

    def moveLeft(self, pMap):
        self.orientation = LEFT
        new_location = (self.location[0] - 1, self.location[1])

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[self.location[1]][self.location[0]] = FLOOR
        else:
            pMap.map[self.location[1]][self.location[0]] = self.under

        self.under = pMap.map[new_location[1]][new_location[0]]
        self.relocate(new_location)

        pMap.map[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveRight(self, pMap):
        self.orientation = RIGHT
        new_location = (self.location[0] + 1, self.location[1])

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[self.location[1]][self.location[0]] = FLOOR
        else:
            pMap.map[self.location[1]][self.location[0]] = self.under

        self.under = pMap.map[new_location[1]][new_location[0]]
        self.relocate(new_location)

        pMap.map[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveUp(self, pMap):
        self.orientation = UP
        new_location = (self.location[0], self.location[1] - 1)

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[self.location[1]][self.location[0]] = FLOOR
        else:
            pMap.map[self.location[1]][self.location[0]] = self.under

        self.under = pMap.map[new_location[1]][new_location[0]]
        self.relocate(new_location)

        pMap.map[new_location[1]][new_location[0]] = PLAYER
        return new_location

    def moveDown(self, pMap):
        self.orientation = DOWN
        new_location = (self.location[0], self.location[1] + 1)

        if not self.under in ELEMENTS and not self.under in SLIDES:
            pMap.map[self.location[1]][self.location[0]] = FLOOR
        else:
            pMap.map[self.location[1]][self.location[0]] = self.under

        self.under = pMap.map[new_location[1]][new_location[0]]
        self.relocate(new_location)

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

class Overlay:
    def __init__(self):
        self.message = "Initial Message"
        self.show = False

    def changeMessage(self, pMsg):
        self.message = pMsg

    def isVisible(self):
        return self.show

    def showOverlay(self):
        self.show = True

    def hideOverlay(self):
        self.show = False 

if __name__ == "__main__":
    main()
