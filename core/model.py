"""Model layer for Conway's Game of Life.

Contains the `GameModel` class, which stores the current state of
the simulation, provides update methods according to Conway's rules,
and notifies subscribers (views) when the state changes.
"""

from __future__ import annotations

import time
from collections.abc import Callable

import numpy as np

from utils.settings import STEP_INTERVAL


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

    # This function runs every tick
    def update(self) -> None:
        """Apply the next generation on the grid."""
        if not self.running:
            return

        now = time.time()
        if now - self.last_update_time < STEP_INTERVAL:
            return  # not yet time for the next step

        self.last_update_time = now
        grid_changed = self.step()
        if not grid_changed:
            print("Pausing run, as simulation has reached a stable state.")
            self.running = False

        self.notify()

    def subscribe(self, callback: Callable[[], None]) -> None:
        """Register a view callback to be called on state updates."""
        self.subscribers.append(callback)

    def notify(self) -> None:
        """Notify all subscribed views."""
        for cb in self.subscribers:
            cb()

    def toggle_cell(self, x: int, y: int) -> None:
        """Toggle a single cell's alive/dead state."""
        self.grid[y, x] = 1 - self.grid[y, x]
        self.notify()

    def step(self) -> bool:
        """Advance the simulation by one generation.

        Returns:
            bool: False if the step hasn't changed anything, True otherwise.
        """
        new_grid = self.compute_next_generation(self.grid)

        self.grid = new_grid
        self.notify()
        if np.array_equal(new_grid, self.grid) or not new_grid.any():
            return False  # returns False, if steps don't change anything
        return True

    def start(self) -> None:
        """Start automatic simulation."""
        self.running = True

    def pause(self) -> None:
        """Pause automatic simulation."""
        self.running = False

    def compute_next_generation(self, current_generation: np.ndarray) -> np.ndarray:
        """Compute the next generation of Conway's Game of Life.

        This function applies Conway's Game of Life rules to the current grid
        using efficient NumPy operations. For each cell in the grid, it counts
        the number of active (alive) neighboring cells by rolling the grid
        across all eight directions. A new grid is then computed according to
        the following rules:

        1. Any live cell with two or three live neighbors survives.
        2. Any dead cell with exactly three live neighbors becomes alive.
        3. All other cells die or remain dead.

        Args:
            current_generation (np.ndarray): A 2D NumPy array representing the
                current state of the grid, where `1` indicates a live cell and
                `0` indicates a dead cell.

        Returns:
            np.ndarray: A new 2D NumPy array of the same shape as the input,
            representing the next generation of the grid.
        """
        new_grid = np.zeros_like(current_generation)
        neighbors = sum(
            np.roll(np.roll(self.grid, i, 0), j, 1)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i != 0 or j != 0)
        )
        new_grid = ((neighbors == 3) | ((self.grid == 1) & (neighbors == 2))).astype(
            int
        )
        return new_grid
