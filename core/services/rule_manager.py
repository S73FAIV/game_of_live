"""Handles unlocking and tracking of Conway's Game of Life rules."""

import numpy as np

from core.view import GameView


class RuleManager:
    """Manages incremental discovery of Conway's Game of Life rules."""

    def __init__(self, view: GameView) -> None:
        self.unlocked: set[str] = set()
        self.view = view

    def update(self, grid: np.ndarray, births: np.ndarray, deaths: np.ndarray) -> None:
        """Analyze the last simulation step and unlock rules if observed.

        Args:
            grid: Current state of the simulation (2D numpy array).
            births: Boolean mask of newly alive cells.
            deaths: Boolean mask of newly dead cells.
        """
        # Rule 1 — Birth condition discovered: dead cell becomes alive.
        if "birth" not in self.unlocked and np.any(births):
            self.unlocked.add("birth")
            self.view.notification_manager.push("Rule discovered: Birth (Reproduction)")
            print("Rule discovered: Birth (Reproduction)")

        # Rule 2 — Survival condition discovered: living cell stays alive.
        # Identify cells that were alive in the previous step and remain alive.
        if "survival" not in self.unlocked:
            # infer survival by difference: if there are alive cells
            # and not all are new births → some persisted
            live_cells = np.count_nonzero(grid)
            if live_cells > 0 and np.count_nonzero(births) < live_cells:
                self.unlocked.add("survival")
                self.view.notification_manager.push("Rule discovered: Survival")
                print("Rule discovered: Survival")

