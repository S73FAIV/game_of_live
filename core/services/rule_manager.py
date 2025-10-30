"""Handles unlocking and tracking of Conway's Game of Life rules."""

import numpy as np

from core.view import GameView
from utils.settings import GRID_HEIGHT, GRID_WIDTH


class RuleManager:
    """Detects and unlocks Conway's fundamental rules when first observed."""

    def __init__(self, view: GameView) -> None:
        self.unlocked: set[str] = set()
        self.view = view

    def update(self, new_grid: np.ndarray, old_grid: np.ndarray) -> None:
        """Evaluate which Life rules are expressed between two consecutive grids."""
        # Compute neighbor counts for the old generation
        neighbors = sum(
            np.roll(np.roll(old_grid, i, 0), j, 1)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i != 0 or j != 0)
        )

        was_alive = old_grid == 1
        is_alive = new_grid == 1

        # Identify cell transitions
        births = (~was_alive) & is_alive
        deaths = was_alive & (~is_alive)

        # Rule 1 – Underpopulation: alive → dead, < 2 neighbors
        if np.any(deaths & (neighbors < 2)) and "Underpopulation" not in self.unlocked:
            self._unlock("Underpopulation", "A lonely cell has died from isolation.")

        # Rule 2 – Survival: alive → alive, 2 or 3 neighbors
        if (
            np.any(is_alive & was_alive & ((neighbors == 2) | (neighbors == 3)))
            and "Survival" not in self.unlocked
        ):
            self._unlock("Survival", "Some cells have stabilized and survived.")

        # Rule 3 – Overpopulation: alive → dead, > 3 neighbors
        if np.any(deaths & (neighbors > 3)) and "Overpopulation" not in self.unlocked:
            self._unlock(
                "Overpopulation", "A crowded area has collapsed from overpopulation."
            )

        # Rule 4 – Reproduction: dead → alive, exactly 3 neighbors
        if np.any(births & (neighbors == 3)) and "Reproduction" not in self.unlocked:
            self._unlock("Reproduction", "New life has emerged from perfect balance.")

    def _unlock(self, key: str, message: str) -> None:
        """Mark rule as unlocked and notify."""
        self.unlocked.add(key)
        self.view.notification_manager.push(message)
        print(message)
