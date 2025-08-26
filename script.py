#!/usr/bin/env python3

import gi
import jdatetime
import cairo
import math
import tempfile
import os
import signal
import sys
import subprocess

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
        # Set up signal handling for clean exit
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.icon_dir = tempfile.mkdtemp()
        self.app_id = "persian-date-indicator"
        
        try:
            self.indicator = AppIndicator3.Indicator.new(
                self.app_id,
                self.create_icon(),
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.menu = self.create_menu()
            self.indicator.set_menu(self.menu)
            
            # Update checks
            GLib.timeout_add_seconds(3600, self.update_date)
            GLib.timeout_add_seconds(60, self.check_date_change)
            
        except Exception as e:
            print(f"Error creating indicator: {e}")
            sys.exit(1)

    def signal_handler(self, signum, frame):
        """Handle signals for clean shutdown"""
        Gtk.main_quit()

    def create_icon(self):
        """Create an icon with the current Persian date number"""
        try:
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
            text = str(day)
            x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = cr.text_extents(text)
            cr.move_to(width/2 - text_width/2 - x_bearing, height/2 + text_height/2)
            
            cr.show_text(text)
            
            # Save to file
            surface.write_to_png(icon_path)
            
            return icon_path
        except Exception as e:
            print(f"Error creating icon: {e}")
            return "calendar"  # Fallback to default calendar icon

    def create_menu(self):
        """Create the context menu for the indicator"""
        menu = Gtk.Menu()
        
        # Full date label
        try:
            self.date_item = Gtk.MenuItem(
                label=jdatetime.datetime.now().strftime("%A, %d %B %Y")
            )
            self.date_item.set_sensitive(False)
            menu.append(self.date_item)
        except:
            pass

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        
        # Gregorian date for reference
        try:
            import datetime
            gregorian_date = Gtk.MenuItem(
                label=datetime.datetime.now().strftime("Gregorian: %Y-%m-%d")
            )
            gregorian_date.set_sensitive(False)
            menu.append(gregorian_date)
        except:
            pass

        separator2 = Gtk.SeparatorMenuItem()
        menu.append(separator2)
        
        # Quit option
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit_application)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def quit_application(self, widget=None):
        """Clean quit function"""
        if hasattr(self, 'icon_dir') and os.path.exists(self.icon_dir):
            import shutil
            shutil.rmtree(self.icon_dir)
        Gtk.main_quit()

    def update_date(self):
        """Update the date display"""
        try:
            new_date = jdatetime.datetime.now().strftime("%A, %d %B %Y")
            self.date_item.set_label(new_date)
        except:
            pass
        return True

    def check_date_change(self):
        """Check if the date has changed and update icon if needed"""
        try:
            day = jdatetime.datetime.now().day
            current_icon = self.indicator.get_icon()
            
            # Extract day from current icon path
            if current_icon and os.path.exists(current_icon):
                try:
                    current_day = int(os.path.basename(current_icon).split('-')[-1].split('.')[0])
                    if day != current_day:
                        new_icon_path = self.create_icon()
                        self.indicator.set_icon(new_icon_path)
                        self.update_date()
                except (ValueError, IndexError):
                    # If we can't parse the current icon, create a new one
                    new_icon_path = self.create_icon()
                    self.indicator.set_icon(new_icon_path)
        except:
            pass
        
        return True

def is_already_running():
    """Simple check to prevent multiple instances"""
    try:
        # Check if any process with our script name is running
        result = subprocess.run(['pgrep', '-f', 'persian-date-indicator'], 
                              capture_output=True, text=True)
        processes = result.stdout.strip().split('\n')
        # Count actual running processes (excluding empty lines)
        running_count = len([p for p in processes if p.strip()])
        
        # If more than 1 process (current one + any existing), we're already running
        return running_count > 1
    except:
        return False

def main():
    # Simple check to prevent multiple instances
    if is_already_running():
        print("Persian Date Indicator is already running")
        sys.exit(0)
    
    # Add a small delay to ensure the desktop environment is fully loaded
    import time
    time.sleep(3)
    
    try:
        indicator = PersianDateIndicator()
        Gtk.main()
    except Exception as e:
        print(f"Error starting Persian Date Indicator: {e}")
    finally:
        # Cleanup on exit
        if 'indicator' in locals() and hasattr(indicator, 'icon_dir'):
            if os.path.exists(indicator.icon_dir):
                import shutil
                shutil.rmtree(indicator.icon_dir)

if __name__ == "__main__":
    main()