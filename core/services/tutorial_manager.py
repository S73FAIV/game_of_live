"""Guides the player through the first steps of Conway's Game of Life."""

import numpy as np

from core.view import GameView
from ui.notification_manager import NotificationType

class TutorialManager:
    """Handles reactive tutorial messages based on player actions and simulation steps."""

    def __init__(self, view: GameView) -> None:
        self.view = view
        self.stage = 0
        self.marker_pos: tuple[int, int] | None = None
        self.active = True
        self.shown_messages: set[str] = set()
        self.highest_triggered_rank = -1

    def update(
        self,
        grid: np.ndarray,
        births: np.ndarray,
        deaths: np.ndarray,
        from_step: bool,
        old_grid: np.ndarray | None = None,
    ) -> None:
        """React to player actions and simulation steps."""
        if not self.active:
            return

        live_cells = int(np.sum(grid))
        n_births = int(np.sum(births))
        n_deaths = int(np.sum(deaths))

        # --- FIRST INTERACTION ---
        if self.stage == 0 and not from_step and n_births > 0:
            self._on_first_cell_created(births)
            self.stage = 1
            return

        # --- SECOND INTERACTION ---
        if self.stage == 1 and from_step and old_grid is not None:
            # Evaluate results based on previously recorded state
            initial = int(np.sum(old_grid))

            # Hierarchical message table: (rank, condition, key, message)
            cases = [
                (
                    0,
                    initial == 1 and live_cells == 0,
                    "one_dying_cell",
                    "It seems a single cell can't survive alone.",
                ),
                (
                    1,
                    initial == 2 and live_cells == 0,
                    "two_dying_cells",
                    "Maybe it needs more cells in its neighbourhood!?",
                ),
                (
                    2,
                    initial == 3 and live_cells == 0,
                    "three_dying_cells",
                    "What do you think happens when you put them all as close together as possible?",
                ),
                (
                    3,
                    initial == 3 and live_cells == 1,
                    "three_with_survivor",
                    "Amazing! It seems one of them survived! How about we just add more cells?!",
                ),
                (
                    4,
                    initial == 3
                    and n_births == 2
                    and n_deaths == 2
                    and live_cells == 3,
                    "blinker",
                    "Wow! It seems to be stable! Congratulation! You created a stable world! \n"
                    "This one will survive on its own after starting the evolution!",
                ),
            ]

            for rank, condition, key, message in cases:
                if (
                    condition
                    and key not in self.shown_messages
                    and rank > self.highest_triggered_rank
                ):
                    self._say(message, key, rank)
                    break  # only one message per frame

    def _on_first_cell_created(self, births: np.ndarray) -> None:
        """Triggered when the first cell is manually placed."""
        y, x = np.argwhere(births)[0]
        self.marker_pos = (int(x), int(y))
        self.initial_live_count = 1

        # Create exclamation marker
        self.view.marker_manager.create_marker(self.marker_pos, symbol="!")

        # Display tutorial intro message
        self.view.notification_manager.push(
            "Wow! You have created life in this desolate place! "
            "Do you think it survives until the next generation?"
        )

        print("Tutorial: First cell created — Stage 1 active.")

    def _say(self, message: str, key: str, rank: int) -> None:
        """Display a tutorial message and update progression."""
        self.view.notification_manager.push(message, NotificationType.TUTORIAL, 6)
        self.shown_messages.add(key)
        self.highest_triggered_rank = max(self.highest_triggered_rank, rank)
        print(f"Tutorial triggered ({key}) → rank {rank}")

    def reset(self) -> None:
        """Reset tutorial state."""
        self.stage = 0
        self.marker_pos = None
        self.active = True
        self.initial_live_count = 0
        self.shown_messages.clear()
        self.highest_triggered_rank = -1
