import signal
import os
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'ipIndicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_ip = gtk.MenuItem('IP')
    item_ip.connect('activate', ip)
    menu.append(item_ip)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def run_command(cmd):
    os.system(cmd + ' > tmp')
    detected = False
    for line in open('tmp', 'r'):
        if detected:
            detected = False
            return line
        if 'eth0' in line:
            detected = True

def fetch_ip():
    return '192.168.*.*'

def ip(_):
    notify.Notification.new("<b>Your IP address</b>", run_command('ifconfig')[20:34], None).show()

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
