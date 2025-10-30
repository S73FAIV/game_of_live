"""Handles unlocking and tracking of Conway's Game of Life rules."""

import numpy as np

from core.view import GameView


class RuleManager:
    """Detects and unlocks Conway's fundamental rules when first observed."""

    def __init__(self, view: GameView, initial_grid: np.ndarray) -> None:
        self.unlocked: set[str] = set()
        self.view = view
        self.prev_grid = initial_grid.copy()

    def update(self, grid: np.ndarray) -> None:
        """Analyze the last simulation step and unlock rules if observed.

        Args:
            grid: Current state of the simulation (2D numpy array).
            births: Boolean mask of newly alive cells.
            deaths: Boolean mask of newly dead cells.
        """
        if self.prev_grid is None:
            self.prev_grid = grid.copy()
            return

        prev = self.prev_grid
        self.prev_grid = grid.copy()

        # Compute neighbor counts for previous generation.
        neighbors = sum(
            np.roll(np.roll(prev, i, 0), j, 1)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i != 0 or j != 0)
        )

        # --- Rule 1: Underpopulation ---
        underpop = (prev == 1) & (neighbors < 2) & (grid == 0)
        if "underpopulation" not in self.unlocked and np.any(underpop):
            self._unlock(
                "underpopulation", "Rule discovered: Underpopulation (lonely cells die)"
            )

        # --- Rule 2: Survival ---
        survival = (prev == 1) & ((neighbors == 2) | (neighbors == 3)) & (grid == 1)
        if "survival" not in self.unlocked and np.any(survival):
            self._unlock(
                "survival", "Rule discovered: Survival (balanced population endures)"
            )

        # --- Rule 3: Overpopulation ---
        overpop = (prev == 1) & (neighbors > 3) & (grid == 0)
        if "overpopulation" not in self.unlocked and np.any(overpop):
            self._unlock(
                "overpopulation", "Rule discovered: Overpopulation (crowding kills)"
            )

        # --- Rule 4: Reproduction ---
        reproduction = (prev == 0) & (neighbors == 3) & (grid == 1)
        if "reproduction" not in self.unlocked and np.any(reproduction):
            self._unlock(
                "reproduction", "Rule discovered: Reproduction (dead cell reborn)"
            )

    def _unlock(self, key: str, message: str) -> None:
        """Mark rule as unlocked and notify."""
        self.unlocked.add(key)
        self.view.notification_manager.push(message)
        print(message)
