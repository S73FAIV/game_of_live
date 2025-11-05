"""Data model for individual rules in the Game of Life."""

from dataclasses import dataclass


@dataclass
class Rule:
    title: str
    description: str
    notification: str
