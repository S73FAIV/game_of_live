"""Manages tutorial progression and onboarding messages."""

import numpy as np

from core.view import GameView


class TutorialManager:
    """Manages tracking of tutorial-messages."""

    view: GameView


    def __init__(self, view: GameView) -> None:
        """Initialize the tutorial manager."""
        self.shown = set()
        self.view = view


    def on_game_start(self, data: dict) -> None:
        if "start_tip" not in self.shown:
            self.shown.add("start_tip")


    def on_generation(self, data: dict) -> None:
        if "progress_tip" not in self.shown and data.get("generation", 0) > 10:
            self.shown.add("progress_tip")

    def update(self, grid: np.ndarray, births: np.ndarray, deaths: np.ndarray) -> None:
        pass
