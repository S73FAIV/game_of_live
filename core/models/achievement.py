from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from ui.colors import ACHIEVEMENT_COLOUR
from ui.icons import ACHIEVEMENT_ICON_PATH


@dataclass(frozen=True)
class Achievement:
    title: str
    description: str
    pattern: np.ndarray
    variants: Sequence[np.ndarray] | None = None
    icon_path: str = ACHIEVEMENT_ICON_PATH
    color: tuple[int, int, int] = ACHIEVEMENT_COLOUR

