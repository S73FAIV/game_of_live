"""Guides the player through the first steps of Conway's Game of Life."""

import numpy as np

from core.services.achievement_manager import AchievementManager
from core.services.rule_manager import RuleManager
from core.view import GameView


class TutorialManager:
    """Handles reactive tutorial messages based on player actions and simulation steps."""

    def __init__(
        self, view: GameView, rules: RuleManager, achievements: AchievementManager
    ) -> None:
        self.view = view
        self.rules = rules
        self.achievements = achievements
        self.stage = 0
        self.marker_pos: tuple[int, int] | None = None
        self.active = True
        self.triggered_messages: set[str] = set()

    def update(
        self, grid: np.ndarray, births: np.ndarray, deaths: np.ndarray, from_step: bool
    ) -> None:
        """React to player actions and simulation steps."""
        if not self.active:
            return

        live_cells = np.sum(grid)
        n_births = births.sum()
        n_deaths = deaths.sum()

        # Stage 0: first cell placement
        if self.stage == 0 and not from_step and n_births > 0:
            self.stage = 1
            self._on_first_cell_created(births)
            return

        # Stage 1: after first placement, handle simulation steps
        if self.stage == 1 and from_step:
            # Hierarchical checks in descending priority

            # Case: 3 cells, blinker discovered
            if (
                "blinker" in self.achievements.unlocked
                and "blinker_tutorial" not in self.triggered_messages
            ):
                self.triggered_messages.add("blinker_tutorial")
                msg = "Wow! It seems to be stable! Congratulation! You created a stable world!"
                if not self.view.state.running:
                    msg += " This one will survive on its own after starting the evolution!"
                self.view.notification_manager.push(msg)
                self.stage = 2
                return

            # Case: 3 cells, at least one survives (triggers survival rule)
            if (
                n_births == 3
                and "Survival" in self.rules.unlocked
                and "three_cells_survive" not in self.triggered_messages
            ):
                self.triggered_messages.add("three_cells_survive")
                self.view.notification_manager.push(
                    "Amazing! What do you think if we add even MORE cells?"
                )
                self.stage = 2
                return

            # Case: 3 cells, all die
            if (
                n_births == 3
                and n_deaths == 3
                and "three_cells_die" not in self.triggered_messages
            ):
                self.triggered_messages.add("three_cells_die")
                self.view.notification_manager.push(
                    "What do you think happens when you put them all as close together as possible?"
                )
                self.stage = 2
                return

            # Case: 2 cells placed
            if n_births == 2 and "two_cells" not in self.triggered_messages:
                self.triggered_messages.add("two_cells")
                self.view.notification_manager.push(
                    "Maybe it needs more cells in its neighbourhood?!"
                )
                self.stage = 2
                return

            # Case: single cell died (underpopulation)
            if (
                n_births == 1
                and "Underpopulation" in self.rules.unlocked
                and "single_cell" not in self.triggered_messages
            ):
                self.triggered_messages.add("single_cell")
                self.view.notification_manager.push(
                    "It seems a single cell can't survive alone."
                )
                self.stage = 2
                return

    def _on_first_cell_created(self, births: np.ndarray) -> None:
        """Triggered when the first cell is manually placed."""
        # locate first new live cell
        y, x = np.argwhere(births)[0]
        self.marker_pos = (int(x), int(y))

        # Tell view to create marker (big exclamation mark)
        self.view.marker_manager.create_marker(self.marker_pos, symbol="!")

        # Show first tutorial message
        self.view.notification_manager.push(
            "Wow, you have created life in this desolate place! "
            "Do you think it survives until the next Generation?"
        )

        print("Tutorial: Stage 1 triggered — first cell created.")

    def reset(self) -> None:
        """Reset tutorial for testing or restart."""
        self.stage = 0
        self.marker_pos = None
        self.active = True
