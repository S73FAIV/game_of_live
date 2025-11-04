"""Generalized Game View for Conway's Game of Life.

Handles rendering orchestration by delegating to specialized UI components.
"""

import pygame

from core.game_model import GameState, UpdateType
from ui.grid import GridRenderer
from ui.marker_manager import MarkerManager
from ui.notification_manager import NotificationManager
from ui.sidebar import Sidebar
from utils.settings import (
    GRID_PIXEL_HEIGHT,
    GRID_PIXEL_WIDTH,
    SIDEBAR_WIDTH,
    TOTAL_HEIGHT,
    TOTAL_WIDTH,
)


class GameView:
    """Central orchestrator for all visual elements in the Game of Life."""

    def __init__(self, state: GameState) -> None:
        """Initialize and register all visual subsystems."""
        self.state = state
        self.screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")

        # Core UI components
        self.grid_renderer = GridRenderer(self.state, self.screen)
        self.sidebar = Sidebar(self.state, self.screen, GRID_PIXEL_WIDTH, 0, SIDEBAR_WIDTH, TOTAL_HEIGHT)
        self.marker_manager = MarkerManager(self.screen)
        self.notification_manager = NotificationManager(self.screen)

        # Possible overlay or additional UI screens (for later)
        self.active_overlay = None  # could hold e.g. SettingsMenu or HelpScreen

        self.state.subscribe(self.on_state_change)


    def draw(self) -> None:
        """Draw all currently active visual components."""
        self.grid_renderer.draw_background()
        self.grid_renderer.draw_grid()
        self.grid_renderer.draw_cells()

        self.marker_manager.draw()
        self.sidebar.draw()
        self.notification_manager.draw()

        if self.active_overlay:
            self.active_overlay.draw()

        pygame.display.flip()

    def on_state_change(self, update_type: UpdateType) -> None:
        """React to model updates by redrawing the view."""
        self.draw()
