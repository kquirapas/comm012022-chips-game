# Chips Game Spin-Off

## Prerequisites

- python 3.8.10
- pygame 2.0.1
- SDL 2.0.14

## Requirements Checklist

### Maps
- [x] Maps are at least 20rows by 40cols
- [x] Load Maps from file
- [x] 4 maps (1 start map, 3 other maps)

### Tiles
- [x] Starting Tile 
- [x] Passable Tile 
- [x] Impassable / Wall Tile
- [x] Locked / Door Tile (Green and Yellow, checks for key in inventory to open)
- [x] Element Tile (Fire and Water)
- [x] Thief Tile (reset to start point, discard all inventory)
- [x] Slide Tile (pushes the player in that direction, not moving)
- [x] Exit Tile


### Items
- [x] Keys (Green and Yellow)
- [x] Element Immunity Item (Fire and Water, max 1, current gets replaced when acquiring new one)

### Player
- [x] Show inventory on screen (update inventory on item pickup)
- [x] Display chips requirement on screen
- [x] Display chips gathered on screen
- [x] Display current immunity on screen
- [x] Move with WASD across map

### Bonus
- [ ] Sound design (bg music and sfx)
- [ ] Press esc to go back to splash screen (restart)

### Progress
20 / 22 (90% Done)
