"""Constants used across the Game of Life simulation."""

# Cells
TILE_SIZE = 16 # Default: 25

# Grid dimensions (in cells)
GRID_WIDTH = 80 # Default: 40
GRID_HEIGHT = 60 # Default: 30
# Grid dimensions (in pixel)
GRID_PIXEL_WIDTH = GRID_WIDTH * TILE_SIZE
GRID_PIXEL_HEIGHT = GRID_HEIGHT * TILE_SIZE
# Sidebar dimensions (in pixels)
SIDEBAR_WIDTH = 200

# Window dimensions
TOTAL_WIDTH = GRID_PIXEL_WIDTH + SIDEBAR_WIDTH
TOTAL_HEIGHT = GRID_PIXEL_HEIGHT

# Game Speed
FPS = 30
STEP_INTERVAL = 0.3  # seconds per simulation step
