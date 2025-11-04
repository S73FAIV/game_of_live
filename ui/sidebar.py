"""Sidebar UI component for Conway's Game of Life.

This module defines the `Sidebar` class, which handles rendering and layout
of the right-hand control panel within the Pygame window.
"""

import pygame

from core.game_model import GameState
from ui.button import Button
from ui.colors import BLACK, WHITE
from utils.settings import SIDEBAR_WIDTH, TOTAL_HEIGHT, TOTAL_WIDTH


class Sidebar:
    """Displays controls and information beside the main grid."""

    def __init__(
        self,
        state: GameState,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Initialize the sidebar component.

        Args:
            state (GameState): Shared game state model for synchronization.
            surface (pygame.Surface): The main Pygame surface to draw on.
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
            "step": Button(
                pygame.Rect(x + 20, y + 50, width - 40, 40), label="Next Generation"
            ),
            "start": Button(
                pygame.Rect(x + 20, y + 100, width - 40, 40), label="Run Evolution"
            ),
            "pause": Button(
                pygame.Rect(x + 20, y + 150, width - 40, 40), label="Stop Evolution"
            ),
            "achievements": Button(
                pygame.Rect(x + 20, y + 210, width - 40, 40),
                label="Achievements",
                toggleable=True,
                accent_color=(255, 100, 0),
            ),
            "rules": Button(
                pygame.Rect(x + 20, y + 260, width - 40, 40),
                label="Rules",
                toggleable=True,
                accent_color=(100, 100, 255),
            ),
            "sound": Button(
                pygame.Rect(x + width - 50, y + height - 50, 32, 32),
                icon_path="assets/img/volume.png",
            ),
            "trash": Button(
                pygame.Rect(x + width - 90, y + height - 50, 32, 32),
                icon_path="assets/img/delete.png",
            ),
        }

    def draw(self) -> None:
        """Render the sidebar UI elements."""
        pygame.draw.rect(self.surface, WHITE, self.rect)
        pygame.draw.rect(self.surface, BLACK, self.rect, width=3)

        for button in self.buttons.values():
            button.draw(self.surface)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Delegate events only if relevant buttons are enabled."""
        for name, button in self.buttons.items():
            if button.handle_event(event):
                # Mutual exclusion: untoggle the other if both are toggleable
                if name in ("achievements", "rules"):
                    other = "rules" if name == "achievements" else "achievements"
                    if self.buttons[other].toggled:
                        self.buttons[other].toggled = False
                return name
        return None

    def set_main_buttons_enabled(self, enabled: bool) -> None:
        """Toggle enabled of main control buttons (step/start/pause)."""
        for key in ("step", "start", "pause", "trash"):
            self.buttons[key].enabled = enabled
