"""Handles drawing the grid and live cells for the Game of Life."""

import pygame

from core.game_model import GameState
from ui.colors import BLACK, LIGHTGRAY, WHITE
from utils.settings import GRID_PIXEL_HEIGHT, GRID_PIXEL_WIDTH, TILE_SIZE


class GridRenderer:
    """Responsible for rendering the main simulation grid and cells."""

    def __init__(self, state: GameState, screen: pygame.Surface) -> None:
        self.state = state
        self.screen = screen

    def draw_background(self) -> None:
        """Fill the grid area background."""
        self.screen.fill(WHITE)

    def draw_grid(self) -> None:
        """Draw black brutalist-style grid lines and a border."""
        line_color = LIGHTGRAY
        line_width = 2
        for x in range(0, GRID_PIXEL_WIDTH + 1, TILE_SIZE):
            pygame.draw.line(
                self.screen, line_color, (x, 0), (x, GRID_PIXEL_HEIGHT), line_width
            )
        for y in range(0, GRID_PIXEL_HEIGHT + 1, TILE_SIZE):
            pygame.draw.line(
                self.screen, line_color, (0, y), (GRID_PIXEL_WIDTH, y), line_width
            )
        pygame.draw.rect(
            self.screen,
            BLACK,
            pygame.Rect(0, 0, GRID_PIXEL_WIDTH, GRID_PIXEL_HEIGHT),
            2,
        )

    def draw_cells(self) -> None:
        """Render all active cells."""
        for y in range(self.state.height):
            for x in range(self.state.width):
                if self.state.grid[y, x] == 1:
                    rect = pygame.Rect(
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    pygame.draw.rect(self.screen, BLACK, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
