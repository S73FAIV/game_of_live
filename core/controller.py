"""Game controller for Conway's Game of Life.

This module handles user input and event management, connecting the
game's model (`GameState`) and view (`GameView`) layers.
"""

import pygame

from core.model import GameState
from core.view import GameView
from utils.settings import TILE_SIZE, GRID_PIXEL_WIDTH


class GameController:
    """Handles user input and controls the flow of the Game of Life.

    The controller listens for Pygame events (mouse clicks, key presses,
    window close actions) and updates the model or view accordingly.
    It also manages the simulation's running state.
    """

    state: GameState
    view: GameView

    def __init__(self, state: GameState, view: GameView) -> None:
        """Initialize the game controller.

        Args:
            state (GameState): The current state of the game grid and rules.
            view (GameView): The rendering view responsible for drawing.
        """
        self.state = state
        self.view = view

    def handle_events(self) -> bool:
        """Process Pygame events such as clicks, keypresses, and window close.

        Handles:
            - Quit events (closes the window)
            - Mouse clicks (toggles cells)
            - Spacebar keypress (starts/stops simulation)

        Returns:
            bool: False if the application should exit, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                if x < GRID_PIXEL_WIDTH:  # inside grid
                    self.handle_grid_interaction(event.pos)
                else:  # inside the sidebar
                    self.handle_sidebarbuttons(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state.running = not self.state.running

        return True

    def handle_grid_interaction(self, pos: tuple[int, int]) -> None:
        """Check if Grid was clicked and act accordingly."""
        x, y = pos
        grid_x = x // TILE_SIZE
        grid_y = y // TILE_SIZE
        self.state.toggle_cell(grid_x, grid_y)

    def handle_sidebarbuttons(self, pos: tuple[int, int]) -> None:
        """Check if any sidebar button was clicked and act accordingly."""
        for name, rect in self.view.sidebar.buttons.items():
            if rect.collidepoint(pos):
                match name:
                    case "start":
                        self.state.start()
                    case "pause":
                        self.state.pause()
                    case "step":
                        self.state.step()
                break
