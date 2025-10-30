"""Handles unlocking and tracking of achievements."""

import numpy as np
from scipy.signal import convolve2d  # for efficient pattern matching

from core.view import GameView



class AchievementManager:
    """Recognizes classic Game of Life patterns and awards achievements."""

    def __init__(self, view: GameView) -> None:
        self.unlocked: set[str] = set()
        self.view = view

        # Define reference patterns (1 = live cell, 0 = dead)
        self.patterns = {
            "block": np.array([[1, 1],
                               [1, 1]]),

            "blinker": np.array([[1, 1, 1]]),

            "glider": np.array([
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ]),

            "loaf": np.array([
                [0, 1, 1, 0],
                [1, 0, 0, 1],
                [0, 1, 0, 1],
                [0, 0, 1, 0]
            ]),
        }

    def update(self, grid: np.ndarray, births: np.ndarray, deaths: np.ndarray) -> None:
        """Search for known patterns in the current grid."""
        for name, pattern in self.patterns.items():
            if name in self.unlocked:
                continue

            if self._contains_pattern(grid, pattern):
                self._unlock(name, f"Achievement unlocked: {name.capitalize()} discovered!")

    def _contains_pattern(self, grid: np.ndarray, pattern: np.ndarray) -> bool:
        """Return True if the grid contains the given pattern anywhere."""
        ph, pw = pattern.shape
        gh, gw = grid.shape

        # simple sliding-window check using correlation
        # match means all live cells of pattern match live cells in grid
        for y in range(gh - ph + 1):
            for x in range(gw - pw + 1):
                sub = grid[y:y+ph, x:x+pw]
                if np.array_equal(sub, pattern):
                    return True
        return False

    def _unlock(self, key: str, message: str) -> None:
        """Record achievement and show notification."""
        self.unlocked.add(key)
        self.view.notification_manager.push(message)
        print(message)