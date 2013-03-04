#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""UI console using urwid library
"""

try:
    import urwid
except ImportError:
    urwid = None



class MainScreen(object):
    """Main user interface, which will contain menus plus games
    """
    palette = [
            ("body", "default", "default"),
            ("foot", "dark cyan", "dark blue", "bold"),
            ("key", "light cyan", "dark blue", "underline"),
            ]

    footer_text = ("foot", [
        "Elohim   ",
        ("key", "F1"), " menu ",
        ("key", "F2"), " options ",
        ])

    def __init__(self):
        self.walker = urwid.SimpleFocusListWalker([])
        listbox = urwid.ListBox(self.walker)
        footer = urwid.AttrWrap(urwid.Text(self.footer_text), "foot")
        self.frame = urwid.Frame(urwid.AttrWrap(listbox, "body"),
                footer=footer)
        self.loop = None

    def main(self):
        """Run main loop
        """
        self.loop = urwid.MainLoop(self.frame, self.palette,
                unhandled_input=self.unhandled_input)
        self.loop.run()

    def make_menu(self, title, choices):
        """Create a main screen menu
        """
        body = [urwid.Text(title), urwid.Divider()]
        for choice, action in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', action)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        menu = urwid.LineBox(
                urwid.ListBox(
                    urwid.SimpleFocusListWalker(
                        body)))
        width = max(choices, key=lambda x: len(x[0]))
        width = max(len(width[0]), len(title))
        self.loop.widget = urwid.Overlay(menu, self.frame,
                align='left',
                width=width + 6,
                height=len(choices) + 4,
                valign='bottom',
                bottom=1
                )


    def main_menu(self):
        """Create the main menu
        """
        def do_exit(_source):
            """callback for quitting program
            """
            raise urwid.ExitMainLoop()

        def do_return(_source):
            """callback for closing menu
            """
            self.loop.widget = self.frame

        self.make_menu('Options', [
            ('Return', do_return),
            ('Quit', do_exit),
            ])

    def unhandled_input(self, key):
        """Handle main screen menu
        """
        if key == "f1":
            self.main_menu()

if __name__ == "__main__":
    MainScreen().main()
