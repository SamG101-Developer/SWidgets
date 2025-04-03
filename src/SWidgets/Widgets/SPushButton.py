from typing import Optional

from PyQt6.QtCore import QAbstractAnimation, pyqtSlot, Qt, QSizeF, QVariantAnimation, QEvent, QVariant
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QPushButton, QWidget

from Gui.SNeumorphismEffect import SNeumorphismEffect
from SWidgets.SApplication import SApplication


class SPushButton(QPushButton):
    _use_small_icon: bool
    _apply_effect: bool
    _hover_animation: QVariantAnimation
    _light_shadow_for_animation: QColor
    _dark_shadow_for_animation: QColor

    def __init__(
            self, parent: Optional[QWidget] = None, small_icon: bool = False, apply_effect: bool = False, *args,
            **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)
        self._use_small_icon = small_icon
        self._apply_effect = apply_effect
        self._init_ui()

    def _init_ui(self):
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet(
            "QPushButton {background-color: transparent; border: none; outline: none;}"
            "QPushButton:menu-indicator {subcontrol-position: bottom right;}")

        if self._apply_effect:
            self.setGraphicsEffect(SNeumorphismEffect(self, SApplication.theme.bg_color, SApplication.theme.light_shadow, SApplication.theme.dark_shadow))
        if self._use_small_icon:
            self.setIconSize(QSizeF(self.geometry().size().width() / 1.5, self.geometry().size().height() / 1.5).toSize())

        self._hover_animation = QVariantAnimation(self)
        self._hover_animation.setDuration(300)
        self._hover_animation.setStartValue(SApplication.theme.bg_color)
        self._hover_animation.setEndValue(SApplication.theme.hover_color)
        self._hover_animation.valueChanged.connect(self._update_button_color)

    @pyqtSlot(QAbstractAnimation.Direction)
    def _animate_hover(self, direction: QAbstractAnimation.Direction) -> None:
        self._hover_animation.setDirection(direction)
        self._hover_animation.start()

    @pyqtSlot(QVariant)
    def _update_button_color(self, color: QColor) -> None:
        if self._apply_effect:
            self.graphicsEffect().set_colors(color, SApplication.theme.light_shadow, SApplication.theme.dark_shadow)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.HoverEnter:
            self._hover_animation.stop()
            self._animate_hover(QAbstractAnimation.Direction.Forward)
        elif event.type() == QEvent.Type.HoverLeave:
            self._hover_animation.stop()
            self._animate_hover(QAbstractAnimation.Direction.Backward)
        return super().event(event)


if __name__ == "__main__":
    import sys
    app = SApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 300, 200)
    window.setStyleSheet(f"background-color: {SApplication.theme.bg_color.name()};")
    button = SPushButton(window, apply_effect=True)
    button.setText("Click Me")
    button.setGeometry(50, 50, 200, 100)
    window.show()
    sys.exit(app.exec())
