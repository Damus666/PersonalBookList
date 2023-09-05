import pygame


class conf:
    w = pygame.display.get_desktop_sizes()[0][0]
    h = pygame.display.get_desktop_sizes()[0][1]
    size = pygame.Vector2(w, h)
    win_center = pygame.Vector2(w//2, h//2)
    fps = 60
    title_fs = 80
    name_fs = 40
    pm_fs = 22
    details_fs = 15

    add_btn_w = w//2+40+5*4
    empty_data = {
        "name": "unknown",
        "editor": "unknown",
        "acquire": "Bought",
        "like": False,
        "forced": False,
        "delegate": "unknown",
        "progress": 0,
        "pages": 100
    }
    acquire_opts = [
        "Bought",
        "Borrowed",
        "Library",
        "Gift"
    ]
