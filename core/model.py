"""Model layer for Conway's Game of Life.

Contains the `GameModel` class, which stores the current state of
the simulation, provides update methods according to Conway's rules,
and notifies subscribers (views) when the state changes.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.settings import STEP_INTERVAL
import numpy as np
import time


class GameState:
    """Stores the state of the grid and controls simulation updates."""

    width: int
    height: int
    grid: np.ndarray
    subscribers: list[Callable[[], None]]

    # for the simulation
    running: bool
    last_update_time: float

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
        self.last_update_time = time.time()
        self.subscribers = []

    def toggle_cell(self, x: int, y: int) -> None:
        """Toggle a single cell's alive/dead state."""
        self.grid[y, x] = 1 - self.grid[y, x]
        self.notify()

    def update(self) -> None:
        """Apply the next generation on the grid."""
        if not self.running:
            return

        now = time.time()
        if now - self.last_update_time < STEP_INTERVAL:
            return  # not yet time for the next step

        self.last_update_time = now
        self.step()
        self.notify()

    def subscribe(self, callback: Callable[[], None]) -> None:
        """Register a view callback to be called on state updates."""
        self.subscribers.append(callback)

    def notify(self) -> None:
        """Notify all subscribed views."""
        for cb in self.subscribers:
            cb()

    def step(self) -> None:
        """Advance the simulation by one generation."""
        neighbors = sum(
            np.roll(np.roll(self.grid, i, 0), j, 1)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i != 0 or j != 0)
        )
        new_grid = ((neighbors == 3) | ((self.grid == 1) & (neighbors == 2))).astype(
            int
        )

        self.grid = new_grid
        self.notify

    def start(self) -> None:
        """Start automatic simulation."""
        self.running = True

    def pause(self) -> None:
        """Pause automatic simulation."""
        self.running = False
