"""Handles temporary tutorial or highlight markers drawn on the grid."""

import pygame
from ui.colors import RED
from utils.settings import TILE_SIZE


class MarkerManager:
    """Draws tutorial or contextual markers over the grid."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.markers: list[dict] = []

    def create_marker(self, pos: tuple[int, int], symbol: str = "!") -> None:
        """Create a new marker at a grid position."""
        x, y = pos
        marker = {
            "pos": (x, y),
            "symbol": symbol,
            "lifetime": 5.0,  # seconds before fadeout (optional)
            "created": pygame.time.get_ticks() / 1000.0,
        }
        self.markers.append(marker)

    def draw(self) -> None:
        """Draw all active markers."""
        now = pygame.time.get_ticks() / 1000.0
        remaining = []

        for m in self.markers:
            elapsed = now - m["created"]
            if elapsed < m["lifetime"]:
                remaining.append(m)
                self._draw_marker(m["pos"], m["symbol"])

        self.markers = remaining

    def _draw_marker(self, pos: tuple[int, int], symbol: str) -> None:
        """Draw a single marker centered above a cell."""
        x, y = pos
        font = pygame.font.SysFont("arial", int(TILE_SIZE * 2), bold=True)
        text = font.render(symbol, True, RED)
        rect = text.get_rect()
        # The follwoing code wants a grid-position instead of a real-position
        # rect.center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE - TILE_SIZE // 2)
        rect.center = (x + TILE_SIZE, y - TILE_SIZE)
        self.screen.blit(text, rect)

    def clear(self) -> None:
        """Remove all markers."""
        self.markers.clear()
