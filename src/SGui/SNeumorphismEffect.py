from typing import Optional

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QConicalGradient, QGradient, QPixmap, QPainter, \
    QTransform, QPainterPath, QPen
from PyQt6.QtWidgets import QGraphicsEffect, QWidget


class SNeumorphismEffect(QGraphicsEffect):
    _corner_shift: tuple[Qt.Corner, Qt.Corner, Qt.Corner, Qt.Corner]
    _shadow_distance: int
    _clip_radius: int
    _base_color: QColor
    _light_shadow_color: QColor
    _dark_shadow_color: QColor
    _origin: Qt.Corner
    _gradient_left: QLinearGradient
    _gradient_top: QLinearGradient
    _gradient_right: QLinearGradient
    _gradient_bottom: QLinearGradient
    _gradient_top_left: Optional[QPixmap]
    _gradient_top_right: Optional[QPixmap]
    _gradient_bottom_left: Optional[QPixmap]
    _gradient_bottom_right: Optional[QPixmap]
    _gradient_radial: QRadialGradient
    _gradient_conical: QConicalGradient
    _light_shadow_stops: list[tuple[int, QColor]]
    _dark_shadow_stops: list[tuple[int, QColor]]
    _corner_stops: list[tuple[int, QColor]]

    def __init__(self, parent: Optional[QWidget], base_color: QColor, light_shadow_color: QColor, dark_shadow_color: QColor, distance: int = 8) -> None:
        super().__init__(parent)
        self._corner_shift = (Qt.Corner.TopLeftCorner, Qt.Corner.TopRightCorner, Qt.Corner.BottomRightCorner, Qt.Corner.BottomLeftCorner)
        self._shadow_distance = distance
        self._clip_radius = 8
        self._base_color = base_color
        self._light_shadow_color = light_shadow_color
        self._dark_shadow_color = dark_shadow_color
        self._origin = Qt.Corner.TopLeftCorner
        self._gradient_left = QLinearGradient(1, 0, 0, 0)
        self._gradient_top = QLinearGradient(0, 1, 0, 0)
        self._gradient_right = QLinearGradient(0, 0, 1, 0)
        self._gradient_bottom = QLinearGradient(0, 0, 0, 1)
        self._gradient_top_left = None
        self._gradient_top_right = None
        self._gradient_bottom_left = None
        self._gradient_bottom_right = None
        self._gradient_radial = QRadialGradient(0.5, 0.5, 0.5)
        self._gradient_conical = QConicalGradient(0.5, 0.5, 0)
        self._init_ui()

    def _init_ui(self) -> None:
        self._gradient_left.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self._gradient_top.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self._gradient_right.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self._gradient_bottom.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self._gradient_radial.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self._gradient_conical.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self._update_colors()
        self._update_origin()
        self._update_distance()
        self.update()

    def _update_colors(self) -> None:
        self._light_shadow_stops = [(0, self._light_shadow_color), (1, Qt.GlobalColor.transparent)]
        self._dark_shadow_stops = [(0, self._dark_shadow_color), (1, Qt.GlobalColor.transparent)]
        self._corner_stops = [(0, self._dark_shadow_color), (0.25, Qt.GlobalColor.transparent), (0.75, Qt.GlobalColor.transparent), (1, self._dark_shadow_color)]

    def _update_origin(self) -> None:
        gradients = [self._gradient_left, self._gradient_top, self._gradient_right, self._gradient_bottom]
        stops = [self._light_shadow_stops, self._light_shadow_stops, self._dark_shadow_stops, self._dark_shadow_stops]
        shift = self._corner_shift.index(self._origin)
        for gradient, sub_stops in zip(gradients, stops[-shift:] + stops[:-shift]):
            gradient.setStops(sub_stops)

    def _update_distance(self) -> None:
        distance = self._shadow_distance + self._clip_radius
        rect = QRectF(0, 0, 2 * distance, 2 * distance)

        light_shadow_stops = self._light_shadow_stops[:]
        dark_shadow_stops = self._dark_shadow_stops[:]
        if self._clip_radius > 0:
            gradient_start = self._clip_radius / (self._shadow_distance + self._clip_radius)
            light_shadow_stops[0] = (gradient_start, self._light_shadow_stops[0][1])
            dark_shadow_stops[0] = (gradient_start, self._dark_shadow_stops[0][1])

        self._gradient_radial.setStops(light_shadow_stops)
        top_left_gradient = self._generate_corner_pixmap(rect, self._gradient_radial)

        self._gradient_conical.setAngle(360)
        self._gradient_conical.setStops(self._corner_stops)
        top_right_gradient = self._generate_corner_pixmap(rect.translated(-distance, 0), self._gradient_radial, self._gradient_conical)

        self._gradient_conical.setAngle(270)
        self._gradient_conical.setStops(self._corner_stops)
        bottom_left_gradient = self._generate_corner_pixmap(rect.translated(0, -distance), self._gradient_radial, self._gradient_conical)

        self._gradient_radial.setStops(dark_shadow_stops)
        bottom_right_gradient = self._generate_corner_pixmap(rect.translated(-distance, -distance), self._gradient_radial)

        images = [top_left_gradient, top_right_gradient, bottom_right_gradient, bottom_left_gradient]
        shift = self._corner_shift.index(self._origin)

        if shift:
            transform = QTransform().rotate(shift * 90)
            for image in images:
                image.swap(image.transformed(transform, Qt.TransformationMode.SmoothTransformation))
        self._gradient_top_left, self._gradient_top_right, self._gradient_bottom_right, self._gradient_bottom_left = images[-shift:] + images[:-shift]

    def _generate_corner_pixmap(self, rect: QRectF, radial_gradient: QRadialGradient, conical_gradient: Optional[QConicalGradient] = None) -> QPixmap:
        corner_pixmap = QPixmap(self._shadow_distance + self._clip_radius, self._shadow_distance + self._clip_radius)
        corner_pixmap.fill(Qt.GlobalColor.transparent)
        corner_painter = QPainter(corner_pixmap)

        if conical_gradient:
            color1 = QColor(conical_gradient.stops()[0][1]); color1.setAlphaF(1)
            color2 = QColor(conical_gradient.stops()[3][1]); color2.setAlphaF(1)
            conical_gradient.setStops([(conical_gradient.stops()[0][0], color1), conical_gradient.stops()[1], conical_gradient.stops()[2], (conical_gradient.stops()[3][0], color2)])

        if self._clip_radius > 0:
            path = QPainterPath()
            path.addRect(rect)
            corner_removal_size = self._clip_radius * 2 - 1
            corner_removal_mask = QRectF(0, 0, corner_removal_size, corner_removal_size)
            corner_removal_mask.moveCenter(rect.center())
            path.addEllipse(corner_removal_mask)
            corner_painter.setClipPath(path)
        corner_painter.fillRect(rect, radial_gradient)

        if conical_gradient:
            corner_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceAtop)
            corner_painter.fillRect(rect, conical_gradient)

        corner_painter.end()
        return corner_pixmap

    def set_colors(self, base_color: QColor, light_shadow_color: QColor, dark_shadow_color: QColor) -> None:
        self._base_color = base_color
        self._light_shadow_color = light_shadow_color
        self._dark_shadow_color = dark_shadow_color
        self._update_colors()
        self._update_origin()
        self._update_distance()
        self.update()

    def boundingRectFor(self, sourceRect: QRectF) -> QRectF:
        distance = self._shadow_distance + 1
        return sourceRect.adjusted(-distance, -distance, distance, distance)

    def draw(self, painter: QPainter) -> None:
        restore_transform = painter.worldTransform()
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        painter.setPen(Qt.PenStyle.NoPen)

        x, y, w, h = self.sourceBoundingRect(Qt.CoordinateSystem.DeviceCoordinates).getRect()
        r = x + w
        b = y + h
        c = self._clip_radius
        d = self._shadow_distance
        e = c * 2

        painter.setWorldTransform(QTransform())

        left_rect = QRectF()
        painter.setBrush(self._gradient_left)
        painter.drawRect(left_rect)

        top_rect = QRectF(x + c, y - d, w - e, d)
        painter.setBrush(self._gradient_top)
        painter.drawRect(top_rect)

        right_rect = QRectF(r, y + c, d, h - e)
        painter.setBrush(self._gradient_right)
        painter.drawRect(right_rect)

        bottom_rect = QRectF(x + c, b, w - e, d)
        painter.setBrush(self._gradient_bottom)
        painter.drawRect(bottom_rect)

        painter.drawPixmap(int(x - d), int(y - d), self._gradient_top_left)
        painter.drawPixmap(int(r - c), int(y - d), self._gradient_top_right)
        painter.drawPixmap(int(r - c), int(b - c), self._gradient_bottom_right)
        painter.drawPixmap(int(x - d), int(b - c), self._gradient_bottom_left)
        painter.setWorldTransform(restore_transform)

        if self._clip_radius > 0:
            path = QPainterPath()
            source, offset = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)
            source_bounds = self.sourceBoundingRect(Qt.CoordinateSystem.DeviceCoordinates)

            painter.save()
            painter.setTransform(QTransform())
            painter.setBrush(self._base_color)
            painter.setPen(QPen(self._dark_shadow_color, 1))

            path.addRoundedRect(source_bounds, self._clip_radius, self._clip_radius)
            painter.setClipPath(path)
            painter.fillPath(path, self._base_color)
            painter.drawPath(path)
            painter.drawPixmap(source.rect().translated(offset), source)
            painter.restore()

        else:
            self.drawSource(painter)
