import pygame
import withui as wui

from conf import conf


class Book:
    def __init__(self, app, data):
        self.app = app
        self.data = data
        self.clamp_progress(True)

        with self.app.main_cont:
            with wui.HCont(margin=0, **wui.INVISIBLE, parent_anchor="center", center_elements=True) as big_cont:
                self.big_cont = big_cont
                with wui.VCont() as cont:
                    self.cont = cont
                    self.name_entry = wui.Entryline(
                        text=self.data["name"], width=conf.w//2, on_change=self.name_change, font_size=conf.name_fs, **wui.INVISIBLE)
                    self.show_btn = wui.Button(
                        text="Show Details", **wui.INVISIBLE, on_click=self.show_details, font_size=conf.details_fs, text_color=(150, 150, 150))
                    with wui.VCont(margin=0, **wui.INVISIBLE, visible=False, active=False) as details_cont:
                        self.details_cont = details_cont
                        with wui.HCont(margin=0, **wui.INVISIBLE):
                            self.progress_entry = wui.Entryline(
                                text=str(self.data["progress"]), width=100, on_change=self.progress_change)
                            self.progress_p = wui.Button(
                                text="+", on_click=self.progress_plus, **wui.INVISIBLE, font_size=conf.pm_fs, parent_anchor="center")
                            self.progress_m = wui.Button(
                                text="-", on_click=self.progress_minus, **wui.INVISIBLE, font_size=conf.pm_fs, parent_anchor="center")
                            wui.Label(text="/")
                            self.pages_entry = wui.Entryline(
                                text=str(self.data["pages"]), width=100, on_change=self.pages_change)
                            self.pages_p = wui.Button(
                                text="+", on_click=self.pages_plus, **wui.INVISIBLE, font_size=conf.pm_fs, parent_anchor="center")
                            self.pages_m = wui.Button(
                                text="-", on_click=self.pages_minus, **wui.INVISIBLE, font_size=conf.pm_fs, parent_anchor="center")
                        with wui.HCont(margin=0, **wui.INVISIBLE):
                            self.acquire_dropdown = wui.DropMenu(options=conf.acquire_opts, selected_option=data["acquire"], min_max_width=conf.w//5, on_select=self.acquire_change)
                            wui.Label(text="Liked: ")
                            self.like_c = wui.Checkbox(
                                size=(30, 30), on_toggle=self.like_change)
                            if self.data["like"]:
                                self.like_c.status.select()
                            wui.Label(text="Forced: ")
                            self.forced_c = wui.Checkbox(
                                size=(30, 30), on_toggle=self.forced_change)
                            if self.data["forced"]:
                                self.forced_c.status.select()
                        with wui.HCont(margin=0, **wui.INVISIBLE):
                            wui.Label(text="Delegator: ")
                            self.delegate_entry = wui.Entryline(
                                text=data["delegate"], width=conf.w//6, on_change=self.delegate_change)
                            wui.Label(text="Editor: ")
                            self.editor_entry = wui.Entryline(
                                text=data["editor"], width=conf.w//6, on_change=self.editor_change)
                        self.hide_btn = wui.Button(
                            text="Hide Details", **wui.INVISIBLE, on_click=self.hide_details, font_size=conf.details_fs, text_color=(150, 150, 150))
                delete_btn = wui.Button(background_image=self.app.main.bin_img,
                                        on_click=self.delete, **wui.Themes.RED, size=(40, 40), background_padding=5)
                wui.ext.HoverGrowAnimation(delete_btn, self.app.main.bin_img)
        
        self.update_outline()

    def get_data(self): return self.data

    def update_outline(self): self.name_entry.set(
        text_color="green" if self.completed else wui.DefaultSettings.text_color)

    def clamp_progress(self, starter=False):
        self.data["progress"] = pygame.math.clamp(
            self.data["progress"], 0, self.data["pages"])
        if not starter:
            self.progress_entry.set(text=str(self.data["progress"]))

    def name_change(self, e): self.data["name"] = self.name_entry.text
    def editor_change(self, e): self.data["editor"] = self.editor_entry.text
    def delegate_change(
        self, e): self.data["delegate"] = self.delegate_entry.text

    def acquire_change(self, option):
        self.data["acquire"] = option

    def like_change(self, e): self.data["like"] = self.like_c.status.selected

    def forced_change(
        self, e): self.data["forced"] = self.forced_c.status.selected

    def progress_change(self, e):
        self.data["progress"] = int(
            self.progress_entry.text) if self.progress_entry.text.isdecimal() else self.data["progress"]
        self.update_outline()
        self.clamp_progress()

    def pages_change(self, e):
        self.data["pages"] = int(
            self.pages_entry.text) if self.pages_entry.text.isdecimal() else self.data["pages"]
        self.update_outline()

    def progress_plus(self, e):
        self.data["progress"] += 1
        self.clamp_progress()
        self.progress_entry.set(text=str(self.data["progress"]))
        self.update_outline()

    def pages_plus(self, e):
        self.data["pages"] += 1
        self.clamp_progress()
        self.pages_entry.set(text=str(self.data["pages"]))
        self.update_outline()

    def progress_minus(self, e):
        self.data["progress"] -= 1
        self.clamp_progress()
        self.progress_entry.set(text=str(self.data["progress"]))
        self.update_outline()

    def pages_minus(self, e):
        self.data["pages"] -= 1
        self.clamp_progress()
        self.pages_entry.set(text=str(self.data["pages"]))
        self.update_outline()

    def delete(self, e):
        self.big_cont.kill()
        self.app.books.remove(self)
        del self

    def show_details(self, e):
        self.details_cont.set(visible=True, active=True)
        self.show_btn.set(visible=False, active=False)

    def hide_details(self, e):
        self.details_cont.set(visible=False, active=False)
        self.show_btn.set(visible=True, active=True)

    @property
    def completed(self):
        return self.data["pages"] <= self.data["progress"]
