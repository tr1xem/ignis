import math
from typing import Literal

import cairo
import gi
from gi.repository.Gdk import RGBA

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ignis.base_widget import BaseWidget
from ignis.gobject import IgnisProperty


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))


class CircularProgressBar(Gtk.DrawingArea, BaseWidget):
    """
    Bases: :class:`Gtk.DrawingArea`

    A circular progress indicator widget.

    Args:
        **kwargs: Properties to set.

    .. code-block:: python

        widgets.CircularProgressBar(
            value=0.75,
            min_value=0,
            max_value=100,
            line_width=6,
            line_style='round',
            pie=False
        )
    """
    __gtype_name__ = "IgnisCircularProgressBar"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        value: float = 1.0,
        min_value: float = 0.0,
        child: Gtk.Widget | None = None,
        max_value: float = 1.0,
        start_angle: float = 0.0,
        end_angle: float = 360.0,
        line_width: int = 4,
        line_style: Literal["none", "butt", "round", "square"]
        | cairo.LineCap = cairo.LineCap.ROUND,
        pie: bool = False,
        invert: bool = False,
        size: tuple[int, int] = (100, 100),
        **kwargs,
    ):
        Gtk.DrawingArea.__init__(self)
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._line_width = line_width
        if isinstance(line_style, str):
            style_map = {
                "none": cairo.LineCap.BUTT,
                "butt": cairo.LineCap.BUTT,
                "round": cairo.LineCap.ROUND,
                "square": cairo.LineCap.SQUARE,
            }
            self._line_style = style_map.get(line_style, cairo.LineCap.ROUND)
        else:
            self._line_style: cairo.LineCap = cairo.LineCap.ROUND

        self._pie = pie
        self._invert = invert
        self.start_angle = start_angle if start_angle is not None else 0.0  # pyright: ignore[reportAttributeAccessIssue]
        self.end_angle = end_angle if end_angle is not None else 360.0  # pyright: ignore[reportAttributeAccessIssue]

        BaseWidget.__init__(self, **kwargs)

        self.set_size_request(size[0], size[1])
        self.set_draw_func(self.__on_draw)

    @IgnisProperty
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value
        self.queue_draw()

    @IgnisProperty
    def min_value(self) -> float:
        return self._min_value

    @min_value.setter
    def min_value(self, value: float) -> None:
        self._min_value = clamp(value, 0.0, self._max_value)
        self.queue_draw()

    @IgnisProperty
    def max_value(self) -> float:
        return self._max_value

    @max_value.setter
    def max_value(self, value: float) -> None:
        if value == 0:
            raise ValueError("max_value cannot be zero")
        self._max_value = value
        self.queue_draw()

    @IgnisProperty
    def pie(self) -> bool:
        return self._pie

    @pie.setter
    def pie(self, value: bool) -> None:
        self._pie = value
        self.queue_draw()

    @IgnisProperty
    def line_width(self) -> int:
        return self._line_width

    @line_width.setter
    def line_width(self, value: int) -> None:
        self._line_width = value
        self.queue_draw()

    @IgnisProperty
    def line_style(self) -> cairo.LineCap:
        return self._line_style

    @line_style.setter
    def line_style(
        self, line_style: Literal["none", "butt", "round", "square"] | cairo.LineCap
    ) -> None:
        if isinstance(line_style, str):
            style_map = {
                "none": cairo.LineCap.BUTT,
                "butt": cairo.LineCap.BUTT,
                "round": cairo.LineCap.ROUND,
                "square": cairo.LineCap.SQUARE,
            }
            self._line_style = style_map.get(line_style, cairo.LineCap.ROUND)
        else:
            self._line_style = line_style
        self.queue_draw()

    @IgnisProperty
    def start_angle(self) -> float:
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value: float) -> None:
        self._start_angle = value
        self.queue_draw()

    @IgnisProperty
    def end_angle(self) -> float:
        return self._end_angle

    @end_angle.setter
    def end_angle(self, value: float) -> None:
        self._end_angle = value
        self.queue_draw()

    @IgnisProperty
    def invert(self) -> bool:
        return self._invert

    @invert.setter
    def invert(self, value: bool) -> None:
        self._invert = value
        self.queue_draw()

    def __on_draw(
        self, drawing_area, cr: cairo.Context, width: int, height: int, user_data=None
    ):
        progress_color = self.get_color()

        track_color = RGBA(0.4, 0.4, 0.4, 1.0)  # pyright: ignore[reportAttributeAccessIssue]

        line_width = self._line_width
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2 - line_width

        if radius <= 0:
            radius = 10

        cr.save()
        cr.set_line_cap(self._line_style)
        cr.set_line_width(line_width)

        cr.set_source_rgba(
            track_color.red, track_color.green, track_color.blue, track_color.alpha
        )
        if self._pie:
            cr.move_to(center_x, center_y)
        cr.arc(
            center_x,
            center_y,
            radius,
            math.radians(self._start_angle),
            math.radians(self._end_angle),
        )
        if self._pie:
            cr.fill()
        else:
            cr.stroke()

        normalized_value = clamp(
            (self._value - self._min_value) / (self._max_value - self._min_value),
            0.0,
            1.0,
        )

        if normalized_value > 0:
            cr.set_source_rgba(
                progress_color.red,
                progress_color.green,
                progress_color.blue,
                progress_color.alpha,
            )
            if self._pie:
                cr.move_to(center_x, center_y)
            cr.arc(
                center_x,
                center_y,
                radius,
                math.radians(self._start_angle),
                math.radians(
                    self._start_angle
                    + normalized_value * (self._end_angle - self._start_angle)
                ),
            )
            if self._pie:
                cr.fill()
            else:
                cr.stroke()

        cr.restore()
