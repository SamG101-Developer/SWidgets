from dataclasses import dataclass

from PyQt6.QtGui import QColor

BASES = {
    "light": "#efefef",
    "dark": "#272727"}

COLORS = {
    "red": "#c80420",
    "orange": "#e44013",
    "yellow": "#fdd500",
    "green": "#3bd65a",
    "teal": "#13cf80",
    "blue": "#4db8ff",
    "purple": "#b286c4"}

ALPHA = 0.32
ALPHA_EX = 0.08
ALPHA_HOVER = 0.4
SHADOW_LIGHT_ADJUST = 28


@dataclass
class STheme:
    name: str
    is_dark: bool
    bg_color: QColor
    fg_color: QColor
    icon_color: QColor
    text_color: QColor
    light_shadow: QColor
    light_shadow_fade: QColor
    dark_shadow: QColor
    dark_shadow_fade: QColor
    hover_color: QColor
    special_bg_color: QColor
    special_icon_color: QColor


def create_theme(base_color: str, color: str) -> STheme:
    is_dark = "dark" in base_color
    base_color, color = QColor(BASES[base_color]), QColor(COLORS[color])

    return STheme(
        name=f"{base_color}-{color}",
        is_dark=is_dark,
        bg_color=QColor(base_color),
        fg_color=QColor("#808080"),
        icon_color=QColor(base_color),
        text_color=QColor("#808080"),
        light_shadow=QColor.fromHsl(base_color.hue(), base_color.saturation(), min(255, base_color.lightness() + SHADOW_LIGHT_ADJUST), int(255 * ALPHA)),
        light_shadow_fade=QColor.fromHsl(base_color.hue(), base_color.saturation(), min(255, base_color.lightness() + SHADOW_LIGHT_ADJUST), int(255 * ALPHA_EX)),
        dark_shadow=QColor.fromHsl(base_color.hue(), base_color.saturation(), max(0, base_color.lightness() - SHADOW_LIGHT_ADJUST), int(255 * ALPHA)),
        dark_shadow_fade=QColor.fromHsl(base_color.hue(), base_color.saturation(), max(0, base_color.lightness() - SHADOW_LIGHT_ADJUST), int(255 * ALPHA_EX)),
        hover_color=QColor.fromHsl(base_color.hue(), base_color.saturation(), max(0, base_color.lightness() - SHADOW_LIGHT_ADJUST // 7), int(255 * ALPHA_HOVER)),
        special_bg_color=QColor(color),
        special_icon_color=QColor(color))
