"""Sidebar UI component for Conway's Game of Life.

This module defines the `Sidebar` class, which handles rendering and layout
of the right-hand control panel within the Pygame window.
"""

import pygame

from core.model import GameState
from ui.colors import BLACK, GRAY, LIGHTGRAY


class Sidebar:
    """Displays controls and information beside the main grid."""

    def __init__(
        self,
        state: GameState,
        surface: pygame.SurfaceType,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Initialize the sidebar component.

        Args:
            state (GameState): Shared game state model for synchronization.
            surface (pygame.SurfaceType): The main Pygame surface to draw on.
            x (int): The x-coordinate of the sidebar's top-left corner.
            y (int): The y-coordinate of the sidebar's top-left corner.
            width (int): The width of the sidebar in pixels.
            height (int): The height of the sidebar in pixels.
        """
        self.state = state
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)

        # Define UI elemt positions
        self.buttons = {
            "start": pygame.Rect(x + 20, y + 50, width - 40, 40),
            "pause": pygame.Rect(x + 20, y + 100, width - 40, 40),
            "step": pygame.Rect(x + 20, y + 150, width - 40, 40),
        }

    def draw(self) -> None:
        """Render the sidebar UI elements."""
        pygame.draw.rect(self.surface, GRAY, self.rect)

        font = pygame.font.SysFont(None, 24)

        pygame.draw.rect(self.surface, LIGHTGRAY, self.buttons["start"])
        pygame.draw.rect(self.surface, LIGHTGRAY, self.buttons["pause"])
        pygame.draw.rect(self.surface, LIGHTGRAY, self.buttons["step"])

        self.surface.blit(
            font.render("Start", 1, BLACK),
            (self.buttons["start"].x + 40, self.buttons["start"].y + 10),
        )
        self.surface.blit(
            font.render("Pause", 1, BLACK),
            (self.buttons["pause"].x + 40, self.buttons["pause"].y + 10),
        )
        self.surface.blit(
            font.render("Step", 1, BLACK),
            (self.buttons["step"].x + 40, self.buttons["step"].y + 10),
        )
