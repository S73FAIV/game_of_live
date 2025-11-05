"""Game controller for Conway's Game of Life.

This module handles user input and event management, connecting the
game's model (`GameState`) and view (`GameView`) layers.
"""

import pygame

from core.game_model import GameState
from core.view import GameView
from utils.settings import GRID_PIXEL_WIDTH, TILE_SIZE


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
        self.first_time = True

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

            # Delegate to sidebar
            sidebar_action = self.view.sidebar.handle_event(event)
            if sidebar_action:
                self.handle_sidebar_action(sidebar_action)
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                if x < GRID_PIXEL_WIDTH:  # inside grid
                    self.handle_grid_interaction(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state.running = not self.state.running

        return True

    def handle_grid_interaction(self, pos: tuple[int, int]) -> None:
        """Check if Grid was clicked and act accordingly."""

        # FIXME: Part of the tutorial had to be moved here
        # Create exclamation marker
        if self.first_time:
            print("Grid interaction triggered once with pos:", pos)
            self.view.marker_manager.create_marker(pos, symbol="!")
            self.first_time = False

        x, y = pos
        grid_x = x // TILE_SIZE
        grid_y = y // TILE_SIZE
        self.state.toggle_cell(grid_x, grid_y)

    def handle_sidebar_action(self, action: str) -> None:
        """Perform logical actions based on sidebar button name."""
        match action:
            case "start":
                self.state.start()
            case "pause":
                self.state.pause()
            case "step":
                self.state.step()
            case "sound":
                self.state.sound.toggle_mute()
            case "trash":
                self.state.clear_grid()
            case "achievements":
                self.state.toggle_view_achievements()
                self.view.sidebar.set_main_buttons_enabled(not self.state.achievements_visible)
            case "rules":
                self.state.toggle_view_rules()
                self.view.sidebar.set_main_buttons_enabled(not self.state.rules_visible)

