#!/usr/bin/env python3

import subprocess
import gi
import jdatetime
gi.require_version('Gtk', '3.0')
try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3
except ValueError:
    # Fallback for newer Ubuntu versions
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3

from gi.repository import Gtk, GObject, GLib

class PersianDateIndicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "persian-date-indicator",
            "calendar",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = self.create_menu()
        self.indicator.set_menu(self.menu)
        GLib.timeout_add_seconds(86400, self.update_date)  # 86400 seconds = 1 day

    def create_menu(self):
        menu = Gtk.Menu()
        self.date_item = Gtk.MenuItem(
            label=jdatetime.datetime.now().strftime("%A, %d %B %Y")
        )
        self.date_item.set_sensitive(False)
        menu.append(self.date_item)

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)

        menu.show_all()
        return menu

    def update_date(self):
        self.date_item.set_label(jdatetime.datetime.now().strftime("%A, %d %B %Y"))
        return True  # return True to keep the timeout going

def main():
    indicator = PersianDateIndicator()
    GObject.threads_init()
    Gtk.main()

if __name__ == "__main__":
    main()