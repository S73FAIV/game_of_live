"""Sidebar UI component for Conway's Game of Life.

This module defines the `Sidebar` class, which handles rendering and layout
of the right-hand control panel within the Pygame window.
"""

import pygame

from core.model import GameState
from ui.colors import BLACK, GRAY


class Sidebar:
    """Represents the sidebar panel in the Game of Life UI.

    The sidebar occupies the right portion of the window and will contain
    buttons, labels, and controls for simulation parameters. Currently, it
    displays a placeholder area and title text.
    """

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

    def draw(self) -> None:
        """Draw the sidebar background and placeholder text."""
        pygame.draw.rect(self.surface, GRAY, self.rect)
        # placeholder text
        font = pygame.font.SysFont(None, 24)
        text = font.render("Sidebar", 1, BLACK)
        self.surface.blit(text, (self.rect.x + 10, self.rect.y + 10))
