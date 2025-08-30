from gi.repository import Gtk, cairo  # type: ignore

import math

from ignis.base_widget import BaseWidget
from ignis.gobject import IgnisProperty
from collections.abc import Callable


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

    def __init__(self, **kwargs):
        Gtk.DrawingArea.__init__(self)

        # Private properties with defaults
        self._value: float = 1.0
        self._min_value: float = 0.0
        self._max_value: float = 1.0
        self._line_width: int = 4
        self._line_style = cairo.LineCap.ROUND  # Set default here, not in property
        self._pie: bool = False
        self._on_change: Callable | None = None

        # Color properties
        self._bg_color: tuple = (0.3, 0.3, 0.3, 1.0)
        self._fg_color: tuple = (0.2, 0.6, 1.0, 1.0)
        self._text_color: tuple = (1.0, 1.0, 1.0, 1.0)
        self._show_text: bool = True

        # Set default size
        self.set_content_width(100)
        self.set_content_height(100)

        # Set up drawing
        self.set_draw_func(self._draw_func)

        BaseWidget.__init__(self, **kwargs)

    def _draw_func(self, area, cr, width, height, user_data=None):
        """Draw function for GTK4 DrawingArea"""

        # Calculate dimensions
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2 - self._line_width - 2

        # Configure cairo
        cr.set_line_width(self._line_width)
        cr.set_line_cap(self._line_style)

        # Draw background circle/ring
        cr.set_source_rgba(*self._bg_color)
        cr.arc(center_x, center_y, radius, 0, 2 * math.pi)

        if self._pie:
            cr.fill_preserve()

        cr.stroke()

        # Calculate progress percentage
        if self._max_value == self._min_value:
            percent = 0.0
        else:
            percent = (self._value - self._min_value) / (self._max_value - self._min_value)
            percent = max(0.0, min(1.0, percent))

        # Draw progress arc/pie
        if percent > 0:
            angle_start = -math.pi / 2  # Start at 12 o'clock
            angle_end = angle_start + 2 * math.pi * percent
            cr.set_source_rgba(*self._fg_color)

            if self._pie:
                # Draw filled pie slice
                cr.move_to(center_x, center_y)
                cr.arc(center_x, center_y, radius, angle_start, angle_end)
                cr.close_path()
                cr.fill()
            else:
                # Draw progress arc
                cr.arc(center_x, center_y, radius, angle_start, angle_end)
                cr.stroke()

        # Draw percentage text
        if self._show_text:
            cr.set_source_rgba(*self._text_color)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            # Scale font size
            font_size = min(width, height) * 0.15
            cr.set_font_size(font_size)
            # Center text
            text = f"{int(percent * 100)}%"
            text_extents = cr.text_extents(text)
            text_x = center_x - text_extents.width / 2 - text_extents.x_bearing
            text_y = center_y + text_extents.height / 2
            cr.move_to(text_x, text_y)
            cr.show_text(text)

    @IgnisProperty
    def value(self) -> float:
        """
        The current progress value.

        Returns:
            float: Current progress.
        """
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        if value is None:
            return

        old_value = self._value
        self._value = float(value)

        if old_value != self._value:
            self.queue_draw()
            if self._on_change:
                self._on_change(self)

    @IgnisProperty
    def min_value(self) -> float:
        """
        Minimum value for this progress bar.

        Returns:
            float: Minimum progress value.
        """
        return self._min_value

    @min_value.setter
    def min_value(self, value: float) -> None:
        if value is None:
            return

        self._min_value = float(value)
        self.queue_draw()

    @IgnisProperty
    def max_value(self) -> float:
        """
        Maximum value for this progress bar.

        Returns:
            float: Maximum progress value.
        """
        return self._max_value

    @max_value.setter
    def max_value(self, value: float) -> None:
        if value is None:
            return

        self._max_value = float(value)
        self.queue_draw()

    @IgnisProperty
    def line_width(self) -> int:
        """
        The width of this progress bar's line in pixels.

        Returns:
            int: Line width in pixels.
        """
        return self._line_width

    @line_width.setter
    def line_width(self, value: int) -> None:
        if value is None:
            return

        self._line_width = int(value)
        self.queue_draw()

    @IgnisProperty  # Removed type annotation to fix enum error
    def line_style(self):
        """
        The style of the line caps.

        Possible values:
        - 'none', 'butt': No line caps
        - 'round': Rounded caps (default)
        - 'square': Square caps

        Returns:
            cairo.LineCap: Line style.
        """
        return self._line_style

    @line_style.setter
    def line_style(self, value) -> None:
        if value is None:
            return

        if isinstance(value, str):
            style_map = {
                'none': cairo.LineCap.BUTT,
                'butt': cairo.LineCap.BUTT,
                'round': cairo.LineCap.ROUND,
                'square': cairo.LineCap.SQUARE,
            }
            value = style_map.get(value.lower(), cairo.LineCap.ROUND)

        self._line_style = value
        self.queue_draw()

    @IgnisProperty
    def pie(self) -> bool:
        """
        Whether to draw as a filled pie chart instead of a ring.

        Returns:
            bool: True if pie chart mode is enabled.
        """
        return self._pie

    @pie.setter
    def pie(self, value: bool) -> None:
        if value is None:
            return

        self._pie = bool(value)
        self.queue_draw()

    @IgnisProperty
    def on_change(self) -> Callable:
        """
        The function to call when the value changes.

        Returns:
            Callable: Callback function.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, value: Callable) -> None:
        self._on_change = value

    def set_colors(self, bg_color=None, fg_color=None, text_color=None):
        """
        Set custom colors for the progress bar.

        Args:
            bg_color (tuple, optional): Background color RGBA.
            fg_color (tuple, optional): Foreground color RGBA.
            text_color (tuple, optional): Text color RGBA.
        """
        if bg_color:
            self._bg_color = bg_color
        if fg_color:
            self._fg_color = fg_color
        if text_color:
            self._text_color = text_color
        self.queue_draw()

    def set_show_text(self, show: bool):
        """
        Toggle percentage text display.

        Args:
            show (bool): Whether to show the percentage text.
        """
        self._show_text = bool(show)
        self.queue_draw()


def create_circular_progress(
    value=1.0,
    min_value=0.0,
    max_value=1.0,
    line_width=4,
    line_style='round',
    pie=False,
    **kwargs
):
    """
    Create CircularProgressBar for Ignis.

    Args:
        value (float): Initial progress value.
        min_value (float): Minimum progress value.
        max_value (float): Maximum progress value.
        line_width (int): Width of the progress line.
        line_style (str): Style of the line caps.
        pie (bool): Whether to draw as a filled pie chart.
        **kwargs: Additional properties.

    Returns:
        CircularProgressBar: A configured CircularProgressBar widget.
    """
    return CircularProgressBar(
        value=value,
        min_value=min_value,
        max_value=max_value,
        line_width=line_width,
        line_style=line_style,
        pie=pie,
        **kwargs
    )
