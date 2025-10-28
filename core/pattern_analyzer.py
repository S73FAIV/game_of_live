"""Analyzes the Game of Life grid for known structures."""

import numpy as np
from services.achievement_manager import AchievementManager
from services.tutorial_manager import TutorialManager


class PatternAnalyzer:
    """Class containing all logic to analyze the patterns in the game-state and emmit events accordingly."""

    def __init__(self) -> None:
        """Initialize the Analyzer with a empty set of detected patterns."""
        self.tutorial_manager = TutorialManager()
        self.achievement_manager = AchievementManager()
        self.detected_patterns = set()

    def analyze(self, grid: np.ndarray) -> None:
        """Check the current grid for known structures and emit pattern events."""
        if self._detect_block(grid) and "block" not in self.detected_patterns:
            self.detected_patterns.add("block")
            # self.tutorial_manager

        if self._detect_glider(grid) and "glider" not in self.detected_patterns:
            self.detected_patterns.add("glider")
            # self.achievement_manager

    def _detect_block(self, grid: np.ndarray) -> bool:
        """Detects a 2x2 still life block."""
        kernel = np.array([[1, 1], [1, 1]])
        for y in range(grid.shape[0] - 1):
            for x in range(grid.shape[1] - 1):
                if np.array_equal(grid[y : y + 2, x : x + 2], kernel):
                    return True
        return False

    def _detect_glider(self, grid: np.ndarray) -> bool:
        """Simple glider detection."""
        glider_patterns = [
            np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]]),
            np.array([[1, 0, 0], [0, 1, 1], [1, 1, 0]]),
        ]
        for pattern in glider_patterns:
            h, w = pattern.shape
            for y in range(grid.shape[0] - h):
                for x in range(grid.shape[1] - w):
                    if np.array_equal(grid[y : y + h, x : x + w], pattern):
                        return True
        return False
