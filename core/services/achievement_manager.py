"""Handles unlocking and tracking of achievements."""

import numpy as np

from core.view import GameView


class AchievementManager:
    """Manages tracking of achievments."""

    view: GameView


    def __init__(self, view: GameView) -> None:
        """Initialize the achievemnt manager."""
        self.unlocked = set()
        self.view = view


    def on_pattern_detected(self, data: dict) -> None:
        """Handle logic, what happens, when a pattern is detected."""
        pattern = data.get("pattern")
        if pattern and pattern not in self.unlocked:
            self.unlocked.add(pattern)
            print(f"🏆 Achievement unlocked: Found {pattern}!")

    def update(self, grid: np.ndarray, births: np.ndarray, deaths: np.ndarray) -> None:
        pass