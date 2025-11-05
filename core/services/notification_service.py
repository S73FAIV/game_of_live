"""Defines the NotificationService interface used by non-UI components."""

from typing import Protocol

import pygame

from ui.notification_manager import NotificationType


class NotificationService(Protocol):
    """Protocol describing a callable that sends notifications to the UI layer."""

    def __call__(
        self,
        ntype: NotificationType,
        message: str,
        duration: float = 3.0,
        item_sprite: pygame.Surface | None = None,
    ) -> None:
        """Display a notification message of a given type.

        Args:
            ntype (NotificationType): The type of notification (Achievement, Rule, Tutorial, etc.).
            message (str): The message to display.
            duration (float, optional): How long to display the message, in seconds.
        """
        ...
