from typing import Optional

from PyQt6.QtWidgets import QWidget

from SWidgets.Gui.SNeumorphismEffect import SNeumorphismEffect
from SWidgets.Widgets.SApplication import SApplication


class SWidget(QWidget):
    _apply_effect: bool

    def __init__(self, parent: Optional[QWidget] = None, apply_effect: bool = False, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self._apply_effect = apply_effect
        self._init_ui()

    def _init_ui(self):
        if self._apply_effect:
            self.setGraphicsEffect(SNeumorphismEffect(self, SApplication.theme.bg_color, SApplication.theme.light_shadow, SApplication.theme.dark_shadow))


if __name__ == "__main__":
    import sys
    app = SApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 300, 200)
    window.setStyleSheet(f"background-color: {SApplication.theme.bg_color.name()};")
    widget = SWidget(window, apply_effect=True)
    widget.setGeometry(50, 50, 200, 100)
    window.show()
    sys.exit(app.exec())
