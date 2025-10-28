"""Game view for Conway's Game of Life.

This module handles all rendering using Pygame, including the grid, cells,
and sidebar interface.
"""

import pygame

from core.game_model import GameState
from ui.colors import BLACK, LIGHTGRAY, WHITE
from ui.notification_manager import NotificationManager
from ui.sidebar import Sidebar
from utils.settings import (
    GRID_PIXEL_HEIGHT,
    GRID_PIXEL_WIDTH,
    SIDEBAR_WIDTH,
    TILE_SIZE,
    TOTAL_HEIGHT,
    TOTAL_WIDTH,
)


class GameView:
    """Renders the Game of Life grid and sidebar using Pygame.

    The view draws the simulation state to the screen and listens for updates
    from the model. It handles drawing the grid lines, live cells, and UI
    elements on the sidebar.
    """

    def __init__(self, state: GameState) -> None:
        """Initialize the game view and prepare the display surface.

        Args:
            state (GameState): The game state object that holds the grid
                and simulation status.
        """
        self.state = state
        self.screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")

        self.sidebar = Sidebar(
            self.state, self.screen, GRID_PIXEL_WIDTH, 0, SIDEBAR_WIDTH, TOTAL_HEIGHT
        )
        self.notification_manager = NotificationManager(self.screen)
        self.state.subscribe(self.draw)

    def draw_grid(self) -> None:
        """Draw the grid lines separating individual cells."""
        # vertical lines
        for x in range(0, GRID_PIXEL_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, GRID_PIXEL_HEIGHT))
        # horizontal lines
        for y in range(0, GRID_PIXEL_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, LIGHTGRAY, (0, y), (GRID_PIXEL_WIDTH, y))

    def draw_cells(self) -> None:
        """Render all active (alive) cells as black squares."""
        for y in range(self.state.height):
            for x in range(self.state.width):
                if self.state.grid[y, x] == 1:
                    rect = pygame.Rect(
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    pygame.draw.rect(self.screen, BLACK, rect)

    def draw(self) -> None:
        """Render the full scene: background, grid, cells, and sidebar."""
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_cells()
        self.sidebar.draw()
        self.notification_manager.draw()
        pygame.display.flip()
