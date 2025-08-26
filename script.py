#!/usr/bin/env python3

import gi
import jdatetime
import cairo
import math
import tempfile
import os

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
        self.icon_dir = tempfile.mkdtemp()
        self.indicator = AppIndicator3.Indicator.new(
            "persian-date-indicator",
            self.create_icon(),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = self.create_menu()
        self.indicator.set_menu(self.menu)
        GLib.timeout_add_seconds(3600, self.update_date)  # Update every hour

    def create_icon(self):
        """Create an icon with the current Persian date number"""
        day = jdatetime.datetime.now().day
        icon_path = os.path.join(self.icon_dir, f"persian-date-{day}.png")
        
        # Create a surface
        width, height = 32, 32
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(surface)
        
        # Draw background circle
        cr.arc(width/2, height/2, min(width, height)/2 - 2, 0, 2 * math.pi)
        cr.set_source_rgb(0.2, 0.4, 0.6)  # Blue background
        cr.fill()
        
        # Draw day number
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(18 if day < 10 else 14)
        cr.set_source_rgb(1, 1, 1)  # White text
        
        # Center text
        if day < 10:
            x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = cr.text_extents(str(day))
            cr.move_to(width/2 - text_width/2 - x_bearing, height/2 + text_height/2)
        else:
            x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = cr.text_extents(str(day))
            cr.move_to(width/2 - text_width/2 - x_bearing, height/2 + text_height/2)
        
        cr.show_text(str(day))
        
        # Save to file
        surface.write_to_png(icon_path)
        
        return icon_path

    def create_menu(self):
        menu = Gtk.Menu()
        
        # Full date label
        self.date_item = Gtk.MenuItem(
            label=jdatetime.datetime.now().strftime("%A, %d %B %Y")
        )
        self.date_item.set_sensitive(False)
        menu.append(self.date_item)

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        
        # Gregorian date for reference
        import datetime
        gregorian_date = Gtk.MenuItem(
            label=datetime.datetime.now().strftime("Gregorian: %Y-%m-%d")
        )
        gregorian_date.set_sensitive(False)
        menu.append(gregorian_date)

        separator2 = Gtk.SeparatorMenuItem()
        menu.append(separator2)
        
        # Quit option
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def update_date(self):
        """Update the date display and icon"""
        # Update the menu label
        new_date = jdatetime.datetime.now().strftime("%A, %d %B %Y")
        self.date_item.set_label(new_date)
        
        # Update the icon if the day has changed
        day = jdatetime.datetime.now().day
        old_icon_path = self.indicator.get_icon()
        old_day = int(os.path.basename(old_icon_path).split('-')[-1].split('.')[0])
        
        if day != old_day:
            new_icon_path = self.create_icon()
            self.indicator.set_icon(new_icon_path)
        
        return True  # return True to keep the timeout going

def main():
    indicator = PersianDateIndicator()
    Gtk.main()

if __name__ == "__main__":
    main()