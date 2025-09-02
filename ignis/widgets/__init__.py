from typing import TypeAlias

from ignis._deprecation import deprecated_getattribute

from .arrow import Arrow
from .arrow_button import ArrowButton
from .box import Box
from .button import Button
from .calendar import Calendar
from .centerbox import CenterBox
from .check_button import CheckButton
from .corner import Corner
from .dropdown import DropDown
from .entry import Entry
from .eventbox import EventBox
from .file_chooser_button import FileChooserButton
from .file_dialog import FileDialog
from .file_filter import FileFilter
from .grid import Grid
from .headerbar import HeaderBar
from .icon import Icon
from .label import Label
from .listbox import ListBox
from .listboxrow import ListBoxRow
from .overlay import Overlay
from .picture import Picture
from .popover_menu import PopoverMenu
from .regular_window import RegularWindow
from .revealer import Revealer
from .revealer_window import RevealerWindow
from .scale import Scale
from .scroll import Scroll
from .separator import Separator
from .spin_button import SpinButton
from .stack import Stack
from .stack_page import StackPage
from .stack_switcher import StackSwitcher
from .switch import Switch
from .toggle_button import ToggleButton
from .window import Window


@deprecated_getattribute(
    """The "Widget" class is deprecated, please use "from ignis import widgets" instead."""
)
class Widget:
    Window: TypeAlias = Window
    Label: TypeAlias = Label
    Button: TypeAlias = Button
    Box: TypeAlias = Box
    Calendar: TypeAlias = Calendar
    Scale: TypeAlias = Scale
    Icon: TypeAlias = Icon
    CenterBox: TypeAlias = CenterBox
    Corner: TypeAlias = Corner
    Revealer: TypeAlias = Revealer
    Scroll: TypeAlias = Scroll
    Entry: TypeAlias = Entry
    Switch: TypeAlias = Switch
    Separator: TypeAlias = Separator
    ToggleButton: TypeAlias = ToggleButton
    RegularWindow: TypeAlias = RegularWindow
    FileChooserButton: TypeAlias = FileChooserButton
    FileFilter: TypeAlias = FileFilter
    Grid: TypeAlias = Grid
    PopoverMenu: TypeAlias = PopoverMenu
    EventBox: TypeAlias = EventBox
    FileDialog: TypeAlias = FileDialog
    HeaderBar: TypeAlias = HeaderBar
    ListBoxRow: TypeAlias = ListBoxRow
    ListBox: TypeAlias = ListBox
    Picture: TypeAlias = Picture
    CheckButton: TypeAlias = CheckButton
    SpinButton: TypeAlias = SpinButton
    DropDown: TypeAlias = DropDown
    Overlay: TypeAlias = Overlay
    Arrow: TypeAlias = Arrow
    ArrowButton: TypeAlias = ArrowButton
    RevealerWindow: TypeAlias = RevealerWindow
    Stack: TypeAlias = Stack
    StackSwitcher: TypeAlias = StackSwitcher
    StackPage = StackPage


__all__ = [
    "Arrow",
    "ArrowButton",
    "Box",
    "Button",
    "Calendar",
    "CenterBox",
    "CheckButton",
    "Corner",
    "DropDown",
    "Entry",
    "EventBox",
    "FileChooserButton",
    "FileDialog",
    "FileFilter",
    "Grid",
    "HeaderBar",
    "Icon",
    "Label",
    "ListBox",
    "ListBoxRow",
    "Overlay",
    "Picture",
    "PopoverMenu",
    "RegularWindow",
    "Revealer",
    "RevealerWindow",
    "Scale",
    "Scroll",
    "Separator",
    "SpinButton",
    "Stack",
    "StackPage",
    "StackSwitcher",
    "Switch",
    "ToggleButton",
    "Window",
]
