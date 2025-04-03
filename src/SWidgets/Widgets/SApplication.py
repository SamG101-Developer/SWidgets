from PyQt6.QtWidgets import QApplication

from SWidgets.Gui.STheme import STheme, create_theme


class SApplication(QApplication):
    theme: STheme = create_theme("dark", "red")

    def __init__(self, argv: list[str]):
        super().__init__(argv)
