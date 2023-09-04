import pygame
import sys
import withui as wui

from conf import conf
from app import App


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(conf.size, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.tt_manager = wui.ext.TooltipManager()

        self.bin_img = pygame.transform.scale_by(
            pygame.image.load("assets/bin.png").convert_alpha(), 0.08)

        self.app = App(self)
        self.app.load()

    def run(self):
        dt = 0
        while True:
            for event in pygame.event.get():
                wui.register_event(event)
                if event.type == pygame.QUIT:
                    self.app.quit()
                    pygame.quit()
                    sys.exit()

            self.screen.fill(0)

            wui.update_ui()
            self.tt_manager.update()
            wui.ext.AnimationsManager.update(dt)
            wui.draw_ui(self.screen)
            dt = self.clock.tick(conf.fps)*0.001
            pygame.display.update()


if __name__ == "__main__":
    Main().run()
