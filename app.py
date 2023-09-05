import pygame
import json
import withui as wui
from conf import conf
from book import Book


class App:
    def __init__(self, main):
        self.main = main
        self.screen: pygame.Surface = main.screen

        with wui.VCont(size=conf.size, **wui.NORESIZE, **wui.SCROLLABLE) as main_cont:
            self.main_cont = main_cont
            self.title_label = wui.Label(
                font_size=conf.title_fs, parent_anchor="center")
            wui.ext.TypingAnimation(
                self.title_label, "Personal Book List").start()

        self.make_add_button()
        self.books: list[Book] = []

    def load(self):
        with open("data/data.json", "r") as file:
            data = json.load(file)
            for book_data in data["books"]:
                self.add_book(book_data)
        self.books = sorted(self.books, key=lambda book: book.completed)

    def save(self):
        self.books = sorted(self.books, key=lambda book: book.completed)
        with open("data/data.json", "w") as file:
            data = {"books": [book.get_data() for book in self.books]}
            json.dump(data, file)

    def add_book(self, book_data):
        self.add_button.kill()
        book = Book(self, book_data)
        self.books.append(book)
        self.make_add_button()

    def make_add_button(self):
        with self.main_cont:
            self.add_button = wui.Button(text="Add Book", width=conf.add_btn_w, auto_resize_h=False,
                                         on_click=self.new_book, parent_anchor="center", **wui.Themes.GREEN)

    def new_book(self, e):
        self.add_book(conf.empty_data.copy())

    def quit(self):
        self.save()
