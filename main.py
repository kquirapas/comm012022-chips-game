
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
PLAYERSIZE = int(0.8 * BLOCKSIZE)
PLAYERMARGIN = int((BLOCKSIZE - PLAYERSIZE) / 2)
INVENTORYSIZE = int(0.8 * BLOCKSIZE)
INVENTORYMARGIN = int((BLOCKSIZE - INVENTORYSIZE) / 2)
INVENTORYTILT = 20

MAPOFFSET = int((SCREENWIDTH - MAPWIDTH * SPRITESIZE) / 2)

def main():
    '''
        Description: initializes the variables, pygame, assets, and runs the entire game.

        Arguments:
            none

        Returns:
            none
    '''

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

    # MAP 0 starting map
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

    # audio
    # load and play bg music indefinitely
    pygame.mixer.music.load("assets/sfx/dungeon.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

    # sfx
    sfx = Sfx()
    sfx.addSound("dead", pygame.mixer.Sound("assets/sfx/dead.wav"))
    sfx.addSound("immune", pygame.mixer.Sound("assets/sfx/immune.wav"))
    sfx.addSound("item", pygame.mixer.Sound("assets/sfx/item.wav"))
    sfx.addSound("thief", pygame.mixer.Sound("assets/sfx/thief.wav"))
    sfx.addSound("unlock", pygame.mixer.Sound("assets/sfx/unlock.wav"))
    sfx.addSound("unlockchip", pygame.mixer.Sound("assets/sfx/unlockchip.wav"))
    sfx.addSound("win", pygame.mixer.Sound("assets/sfx/win.wav"))
    sfx.addSound("slide", pygame.mixer.Sound("assets/sfx/slide.wav"))
    sfx.setVolume(0.5)

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
                    if checkNextTile(player, mapholder, maplist, UP, overlay, sfx):
                        if (player.under in SLIDES):
                            sfx.playSound("slide")

                            SMOVE[player.under](mapholder)
                        else:
                            player.relocate(player.moveUp(mapholder))
                elif event.key == pygame.K_a:
                    if checkNextTile(player, mapholder, maplist, LEFT, overlay, sfx):
                        if (player.under in SLIDES):
                            sfx.playSound("slide")

                            SMOVE[player.under](mapholder)
                        else:
                            player.relocate(player.moveLeft(mapholder))
                elif event.key == pygame.K_s:
                    if checkNextTile(player, mapholder, maplist, DOWN, overlay, sfx):
                        if (player.under in SLIDES):
                            sfx.playSound("slide")

                            SMOVE[player.under](mapholder)
                        else:
                            player.relocate(player.moveDown(mapholder))
                elif event.key == pygame.K_d:
                    if checkNextTile(player, mapholder, maplist, RIGHT, overlay, sfx):
                        if (player.under in SLIDES):
                            sfx.playSound("slide")

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
                # if there is overlay message
                if event.key == pygame.K_r:
                    restartLevel(player, mapholder, overlay)
                elif event.key == pygame.K_ESCAPE:
                    restartGame(player, mapholder, map0, overlay)
                elif event.key == pygame.K_SPACE and player.clear and maplist:
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
                        if player.under in ITEMS or player.under in IMMUNITY or player.under in DOORS or player.under == CHIPTILE:
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

                        screen.blit(pygame.transform.scale(player_sprite, (PLAYERSIZE, PLAYERSIZE)), ((col - col_start) * BLOCKSIZE + PLAYERMARGIN, (row - row_start) * BLOCKSIZE + PLAYERMARGIN))

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
        controlsText = overlayFont.render("[ M ] Map    [ R ] Restart Level    [ ESC ] Restart Game    [ Q ] Quit", False, WHITE)
        controlsTextRect = controlsText.get_rect()
        controlsTextRect.center = (SCREENWIDTH // 2, BLOCKSIZE // 2)
        screen.blit(controlsText, controlsTextRect)

        # update display with pygame
        pygame.display.flip()


def checkNextTile(pPlayer, pMap, pMapList, pDir, pOverlay, pSfx):
    '''
        Description: Every time a player moves, it checks the tile it will land on. It checks if it's passable, impassable, and what type of tile it is. It invokes the related functions that corresponds to the expected behavior of that tile

        Arguments:
            pPlayer     Player() object that holds the information related to the player. This is where the player is adjusted depending on the behavior of the tile
            pMap        Map() object that holds the 2D list of the map and map functions. For manipulating the map depending on the tile's behavior
            pMapList    List of Map() objects that are currently available for play in the current run of the game. Used for moving on to the next level
            pDir        Tuple that signifies what direction of movement was taken. Used for tile checking and evaluation
            pOverlay    Overlay() object managing the information needed to display the overlay. Used for changing what message is displayed when changing levels, death, win, etc.
            pSfx        Holds the sound effects. Plays the sound when player interacts with an interactive tile

        Returns:
            ret1        Bool (True or False) signifiying whether the movement may continue as evaluated by the function. (If passable and valid)
    '''

    # check next location for enemies, items, etc.
    # updates map and player (inventory) accordingly
    next_tile = pMap.map[pPlayer.location[1] + pDir[1]][pPlayer.location[0] + pDir[0]]

    if next_tile == WALL:
        return False
    elif next_tile in DOORS:
        if next_tile == GREENDOOR and GREENKEY in pPlayer.inventory:
            pSfx.playSound("unlock")

            pPlayer.removeItem(GREENKEY)
            return True
        elif next_tile == YELLOWDOOR and YELLOWKEY in pPlayer.inventory:
            pSfx.playSound("unlock")

            pPlayer.removeItem(YELLOWKEY)
            return True
        elif next_tile == CHIPDOOR:
            if pMap.chips <= pPlayer.chips:
                pSfx.playSound("unlockchip")

                return True

        return False
    elif next_tile in ITEMS:
        pSfx.playSound("item")

        if next_tile == GREENKEYTILE:
            pPlayer.addItem(GREENKEY)
        elif next_tile == YELLOWKEYTILE:
            pPlayer.addItem(YELLOWKEY)
        return True
    elif next_tile in IMMUNITY:
        pSfx.playSound("immune")

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
            # sfx 
            pSfx.playSound("dead")

            lose(pOverlay)
    elif next_tile == THIEF:
        pSfx.playSound("thief")

        restartLevel(pPlayer, pMap, pOverlay)
        return False
    elif next_tile == EXIT:
        pSfx.playSound("win")

        win(pPlayer, pMap, pMapList, pOverlay)
        return False
    elif next_tile == CHIPTILE:
        pSfx.playSound("item")

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

        return checkNextTile(pPlayer, pMap, pMapList, SDIR[next_tile], pOverlay, pSfx)
    else:
        return True

def restartLevel(pPlayer, pMap, pOverlay):
    '''
        Description: A function that restarts the CURRENT level and reloads the related variables to the current level

        Arguments:
            pPlayer        Holds information about the player and is used for updating positiong, orientation, etc after restart
            pMap           Holds the map information. Used for restarting and reloading the map to its original state
            pOverlay       Holds the message to be displayed during an overlay event. Used to reset and hide overlay.

        Returns:
            No return
    '''

    pOverlay.hideOverlay()
    pPlayer.orientation = DOWN
    pPlayer.clearInventory()
    pPlayer.clearImmunity()
    pPlayer.clearChips()
    pMap.load(pPlayer)

def restartMapList(pAllMaps, pMapList):
    '''
        Description: Function used for reloading all the maps again into the game map list when the ENTIRE GAME is restarted

        Arguments:
            pAllMaps        List holding all the available maps for the game
            pMapList        List holding the current available maps for the game. This is where pAllMaps is transferred for restarting of the game.

        Returns:
            No return
    '''

    pMapList.clear()
    for m in pAllMaps:
        pMapList.append(m)

def restartGame(pPlayer, pMap, pStartMap, pOverlay):
    '''
        Description: Function used for restarting the ENTIRE GAME and resetting all related and needed variables for game restart

        Arguments:
            pPlayer        Holds information about the player and is used for updating positiong, orientation, etc after restart
            pMap           Holds the map information. Used for restarting and reloading the map to its original state
            pStartMap      The specified map to start on every time the game is started
            pOverlay       Holds the message to be displayed during an overlay event. Used to reset and hide overlay.


        Returns:
            No return
    '''

    pOverlay.hideOverlay()
    pMap.swap(pPlayer, pStartMap.name, pStartMap.filepath)
    restartLevel(pPlayer, pMap, pOverlay)

def nextLevel(pPlayer, pMap, pMapList, pOverlay):
    '''
        Description: Function that moves the game to the next level by reloading maps, players, overlays, maplist, etc

        Arguments:
            pPlayer        Holds information about the player and is used for updating positiong, orientation, etc after restart
            pMap           Holds the map information. Used for restarting and reloading the map to its original state
            pMapList        List holding the current available maps for the game. This is where pAllMaps is transferred for restarting of the game.
            pOverlay       Holds the message to be displayed during an overlay event. Used to reset and hide overlay.


        Returns:
            No return
    '''

    # remove current map from map list
    index = 0
    for m in range(len(pMapList)):
        if pMap.name == pMapList[m].name:
            index = m
    del pMapList[index]

    # randomly choose from available maps
    if pMapList:
        choice = random.choice(pMapList)
        pMap.swap(pPlayer, choice.name, choice.filepath)
        restartLevel(pPlayer, pMap, pOverlay)
    else:
        win(pPlayer, pMap, pMapList, pOverlay)

def lose(pOverlay):
    '''
        Description: Function to change the overlay message to show and intiates an Overlay in the event of a lost (death in the game)

            pOverlay       Holds the message to be displayed during an overlay event. Used to reset and hide overlay.

        Returns:
            No return
    '''

    # display lost in overlay
    pOverlay.showOverlay()
    pOverlay.changeMessage("You lost!")

def win(pPlayer, pMap, pMapList, pOverlay):
    '''
        Description: A function that modifies the overlay message to display a win when winning the entire game or clearing the current level

        Arguments:
            pPlayer        Holds information about the player and is used for updating positiong, orientation, etc after restart
            pMap           Holds the map information. Used for restarting and reloading the map to its original state
            pMapList        List holding the current available maps for the game. This is where pAllMaps is transferred for restarting of the game.
            pOverlay       Holds the message to be displayed during an overlay event. Used to reset and hide overlay.


        Returns:
            No return
    '''

    # display win in overlay
    if len(pMapList) == 0:
        pOverlay.showOverlay()
        pOverlay.changeMessage("You won! All levels completed!")
    else:
        pPlayer.clear = True
        pOverlay.showOverlay()
        pOverlay.changeMessage("Map cleared! Press SPACE to continue")


# classes
class Player:
    def __init__(self):
        '''
            Description: Function to initialize player object

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.orientation = DOWN
        self.clear = False
        self.location = (0, 0)
        self.chips = 0
        self.immunity = 0
        self.under = 0
        self.inventory = []

    def relocate(self, pLoc):
        '''
            Description: A function for relocating the player to desired location given with the tuple pLoc

            Arguments:
                self        a reference to itself
                pLoc        a tuple to where the player is relocated to

            Returns:
                No return
        '''

        self.location = pLoc

    def moveLeft(self, pMap):
        '''
            Description:   A function to displace the player to the left in the map

            Arguments:
                self        a reference to itself
                pMap        Map() object holding the information of the current map loaded in the current game

            Returns:
                ret1        A tuple of the player's new location
        '''

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
        '''
            Description:   A function to displace the player to the right in the map

            Arguments:
                self        a reference to itself
                pMap        Map() object holding the information of the current map loaded in the current game

            Returns:
                ret1        A tuple of the player's new location
        '''

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
        '''
            Description:   a function to displace the player to the up in the map

            Arguments:
                self        a reference to itself
                pMap        Map() object holding the information of the current map loaded in the current game

            Returns:
                ret1        a tuple of the player's new location
        '''

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
        '''
            Description:   a function to displace the player to the down in the map

            Arguments:
                self        a reference to itself
                pMap        Map() object holding the information of the current map loaded in the current game

            Returns:
                ret1        a tuple of the player's new location
        '''

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
        '''
            Description:    a function to empty the player's inventory

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.inventory = []

    def clearImmunity(self):
        '''
            Description:    a function to clear the player's immunity

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.immunity = 0

    def clearChips(self):
        '''
            Description:    a function to clear the player's chips count

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.chips = 0

    def addChip(self):
        '''
            Description:    a function to increment the player's chips count

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.chips += 1

    def addItem(self, pItem):
        '''
            Description:    a function to add an item to the player's inventory

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.inventory.append(pItem)

    def removeItem(self, pItem):
        '''
            Description:    a function to remove an item from the player's inventory

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.inventory.remove(pItem)


class Map:
    def __init__(self, name, filepath):
        '''
            Description:    a function to initialize Map object

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.name = name
        self.filepath = filepath
        self.chips = 0
        self.map = []

    def load(self, player):
        '''
            Description:    A function to read from the specified map file (csv format) and load it into the Map object

            Arguments:
                self        a reference to itself
                player      Player() object that holds the player information. Used for relocating player into specified position in the map file

            Returns:
                No return
        '''

        self.map = []
        map_file = open(self.filepath)

        curr_line = map_file.readline()
        self.chips = int(curr_line.split(",")[0])

        curr_line = map_file.readline()
        curr_line_split =  curr_line.split(",")
        player.relocate((int(curr_line_split[0]), int(curr_line_split[1])))
        player.under = 0

        curr_line = map_file.readline()
        while curr_line:
            self.map.append([int(cell) for cell in curr_line.split(",")])
            curr_line = map_file.readline()
        map_file.close()

    def swap(self, pPlayer, name, filepath):
        '''
            Description:    A function to swap current map with another map

            Arguments:
                self        a reference to itself
                pPlayer     Holds the player information. Used for relocating player into specified position in the map file
                name        String that holds the name of the map to be swapped in the current map
                filepath    String that holds the file location of the map to be swapped to

            Returns:
                No return
        '''

        self.name = name
        self.filepath = filepath
        self.load(pPlayer)

class Overlay:
    def __init__(self):
        '''
            Description:    A function to initialize Overlay object

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.message = "Initial Message"
        self.show = False

    def changeMessage(self, pMsg):
        '''
            Description:    A function to change the message be displayed in the overlay

            Arguments:
                self        a reference to itself
                pMsg        String that holds the message to use in the overlay

            Returns:
                No return
        '''

        self.message = pMsg

    def isVisible(self):
        '''
            Description:    A function to check if the overlay is currently visible

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        return self.show

    def showOverlay(self):
        '''
            Description:    A function to show the overlay

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.show = True

    def hideOverlay(self):
        '''
            Description:    A function to hide the overlay

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.show = False 

class Sfx:
    def __init__(self):
        '''
            Description:    A function to initialize Sfx object

            Arguments:
                self        a reference to itself

            Returns:
                No return
        '''

        self.sounds = {}
        self.volume = 1

    def addSound(self, pName, pSfx):
        '''
            Description:    A function to add a new sound to the Sfx object

            Arguments:
                self        a reference to itself
                pName       String that holds the name to be used as key when the specific sounds needs to be played
                pSfx        A pygame.mixer.Sound() object that holds the sound. Used for referencing the pygame sound object when needed (e.g. playing sound)

            Returns:
                No return
        '''

        self.sounds[pName] = pSfx
        self.sounds[pName].set_volume(self.volume)

    def playSound(self, pName):
        '''
            Description:    A function to play the specified sound

            Arguments:
                self        a reference to itself
                pName       String that holds the name to be used as key when playing the specific sound

            Returns:
                No return
        '''

        self.sounds[pName].play()

    def setVolume(self, pVol):
        '''
            Description:    A function to set the volume of all the currently existing sound in the Sfx object

            Arguments:
                self        a reference to itself
                pVol        Float representing the volume level to be set to (0 - 1.0)

            Returns:
                No return
        '''

        self.volume = pVol
        for k, v in self.sounds.items():
            v.set_volume(self.volume)



if __name__ == "__main__":
    main()
