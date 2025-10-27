"""Sidebar UI component for Conway's Game of Life.

This module defines the `Sidebar` class, which handles rendering and layout
of the right-hand control panel within the Pygame window.
"""

import pygame

from core.model import GameState
from ui.colors import BLACK, GRAY, LIGHTGRAY
from utils.settings import TOTAL_HEIGHT, TOTAL_WIDTH, SIDEBAR_WIDTH


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

        # Define UI elemet positions
        self.buttons = {
            "start": pygame.Rect(x + 20, y + 50, width - 40, 40),
            "pause": pygame.Rect(x + 20, y + 100, width - 40, 40),
            "step": pygame.Rect(x + 20, y + 150, width - 40, 40),
            "sound": pygame.Rect(x + SIDEBAR_WIDTH - 50, y + TOTAL_HEIGHT - 50, 32, 32), # lower right corner
            "trash": pygame.Rect(x + SIDEBAR_WIDTH - 90, y + TOTAL_HEIGHT - 50, 32, 32) # lower right corner
        }

        self.sound_on_icon = pygame.image.load("assets/img/volume.png").convert_alpha()
        self.sound_off_icon = pygame.image.load("assets/img/mute.png").convert_alpha()
        # scale icons to fit the button if necessary
        self.sound_on_icon = pygame.transform.smoothscale(self.sound_on_icon, (32, 32))
        self.sound_off_icon = pygame.transform.smoothscale(self.sound_off_icon, (32, 32))
        # TODO: do trash icon
        self.trash_icon = pygame.transform.smoothscale(self.sound_off_icon, (32, 32))


    def draw(self) -> None:
        """Render the sidebar UI elements."""
        pygame.draw.rect(self.surface, GRAY, self.rect)

        font = pygame.font.SysFont(None, 24)

        for name, rect in self.buttons.items():
            pygame.draw.rect(self.surface, LIGHTGRAY, rect)

            if name == "sound":
                icon = self.sound_off_icon if self.state.sound.muted else self.sound_on_icon
                self.surface.blit(icon, rect)
            elif name == "trash":
                icon = self.trash_icon
            else:
                self.surface.blit(
                    font.render(name.capitalize(), 1, BLACK),
                    (rect.x + 40, rect.y +10)
                )


