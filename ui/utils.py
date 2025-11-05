import pygame

def tint_surface(surface: pygame.Surface, tint_color: tuple[int, int, int]) -> pygame.Surface:
    """Return a tinted copy of a surface while preserving alpha."""
    tinted = surface.copy()
    tinted.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
    tint_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    tint_overlay.fill((*tint_color, 0))
    tinted.blit(tint_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return tinted