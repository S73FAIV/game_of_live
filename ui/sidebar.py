"""Sidebar UI component for Conway's Game of Life.

This module defines the `Sidebar` class, which handles rendering and layout
of the right-hand control panel within the Pygame window.
"""

import pygame

from core.model import GameState
from ui.colors import BLACK, GRAY, WHITE


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
        self.button_step = pygame.Rect(x+20, y+20, width -40, 40)

    def draw(self) -> None:
        """Render the sidebar UI elements."""
        pygame.draw.rect(self.surface, GRAY, self.rect)
        
        # Step Button
        pygame.draw.rect(self.surface, WHITE, self.button_step)
        pygame.draw.rect(self.surface, BLACK, self.button_step, width=2)

        font = pygame.font.SysFont(None, 24)
        text = font.render("Step", 1, BLACK)
        text_rect = text.get_rect(center=self.button_step.center)
        self.surface.blit(text, text_rect)
