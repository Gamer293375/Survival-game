import arcade

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE
)

from views.menu import MenuView

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView(window)
    window.show_view(menu)
    arcade.run()

main()