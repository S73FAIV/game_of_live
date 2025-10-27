"""Handles all dynamic UI components such as popups and overlays."""

import pygame

from ui.popup import Popup


class NotificationManager:
    popup_queue: list[Popup]

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.active_popup: Popup | None = None

    def add_notification(self, new_popup: Popup) -> None:
        pass

    def draw(self) -> None:
        pass
