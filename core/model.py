"""Model layer for Conway's Game of Life.

Contains the `GameModel` class, which stores the current state of
the simulation, provides update methods according to Conway's rules,
and notifies subscribers (views) when the state changes.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


class GameState:
    """Stores the state of the grid and controls simulation updates."""

    width: int
    height: int
    grid: np.ndarray
    running: bool
    subscribers: list[Callable[[], None]]

    def __init__(self, width: int = 50, height: int = 30) -> None:
        """Initialize a new Game of Life model.

        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.running = False
        self.subscribers = []

    def toggle_cell(self, x: int, y: int) -> None:
        """Toggle a single cell's alive/dead state."""
        self.grid[y, x] = 1 - self.grid[y, x]
        self.notify()

    def update(self) -> None:
        """Apply the next generation on the grid."""
        if not self.running:
            return
        new_grid = self.grid.copy()
        # Apply Conway's rules here (to be implemented later)
        self.grid = new_grid
        self.notify()

    def subscribe(self, callback: Callable[[], None]) -> None:
        """Register a view callback to be called on state updates."""
        self.subscribers.append(callback)

    def notify(self) -> None:
        """Notify all subscribed views."""
        for cb in self.subscribers:
            cb()
