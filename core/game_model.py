"""Model layer for Conway's Game of Life.

Contains the `GameModel` class, which stores the current state of
the simulation, provides update methods according to Conway's rules,
and notifies subscribers (views) when the state changes.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

import numpy as np

from core.services.sound_manager import SoundManager
from utils.settings import GRID_HEIGHT, GRID_WIDTH, STEP_INTERVAL

if TYPE_CHECKING:
    from collections.abc import Callable


class GameState:
    """Stores the state of the grid and controls simulation updates."""

    width: int
    height: int
    total_cells: int
    grid: np.ndarray
    births: np.ndarray
    deaths: np.ndarray
    subscribers: list[Callable[[], None]]

    # for the simulation
    running: bool
    last_update_time: float
    sound: SoundManager

    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT) -> None:
        """Initialize a new Game of Life model.

        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
        """
        # the size
        self.width = width
        self.height = height
        self.total_cells = width * height
        # the grid
        self.grid = np.zeros((height, width), dtype=int)
        self.births = np.zeros((height, width), dtype=int)
        self.deaths = np.zeros((height, width), dtype=int)
        # the simulation
        self.running = False
        self.last_update_time = time.time()
        # sound
        self.sound = SoundManager()
        self.sound.play_music()
        # model-controller-view
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
        if not self.step():
            print("Pausing run, as simulation has reached a stable state.")
            self.running = False


    def subscribe(self, callback: Callable[[], None]) -> None:
        """Register a view callback to be called on state updates."""
        self.subscribers.append(callback)

    def notify(self) -> None:
        """Notify all subscribed views."""
        for cb in self.subscribers:
            cb()

    def toggle_cell(self, x: int, y: int) -> None:
        """Toggle a single cell's alive/dead state."""
        old_grid = self.grid.copy()
        # the actual update of the cell
        self.grid[y, x] = 1 - self.grid[y, x]

        self.births = (self.grid == 1) & (old_grid == 0)
        self.deaths = (self.grid == 0) & (old_grid == 1)
        n_births = np.sum(self.births)
        n_deaths = np.sum(self.deaths)
        live_cells = np.sum(self.grid)
        # Trigger Sounds relative to GameState
        self.sound.play_generation_batch(
            n_births, n_deaths, live_cells, self.total_cells
        )
        self.notify()

    def step(self) -> bool:
        """Advance the simulation by one generation.

        Returns:
            bool: False if the step hasn't changed anything, True otherwise.
        """
        old_grid = self.grid.copy()
        new_grid = self.compute_next_generation(self.grid)

        # Sound effects
        # Identify births and deaths
        self.births = (new_grid == 1) & (old_grid == 0)
        self.deaths = (new_grid == 0) & (old_grid == 1)
        n_births = np.sum(self.births)
        n_deaths = np.sum(self.deaths)

        live_cells = np.sum(self.grid)
        # Trigger Sounds relative to GameState
        self.sound.play_generation_batch(
            n_births, n_deaths, live_cells, self.total_cells
        )

        self.grid = new_grid
        # Analyze the current generation
        self.notify()

        changed = not np.array_equal(new_grid, old_grid)
        return changed and bool(new_grid.any())

    def start(self) -> None:
        """Start automatic simulation."""
        self.running = True

    def pause(self) -> None:
        """Pause automatic simulation."""
        self.running = False

    def clear_grid(self) -> None:
        """Clear grid (kill all living cells)."""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.notify()

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
