#!/usr/bin/env python

import sys

from gi.repository import Gtk
from kiwi.ui.hyperlink import HyperLink
from kiwi.ui.objectlist import ObjectList, ObjectTree
from kiwi.ui.widgets.label import ProxyLabel
from kiwi.ui.widgets.combo import ProxyComboEntry, ProxyComboBox
from kiwi.ui.widgets.checkbutton import ProxyCheckButton
from kiwi.ui.widgets.radiobutton import ProxyRadioButton
from kiwi.ui.widgets.entry import ProxyEntry, ProxyDateEntry
from kiwi.ui.widgets.spinbutton import ProxySpinButton
from kiwi.ui.widgets.textview import ProxyTextView
from kiwi.ui.widgets.button import ProxyButton


# pylint: disable=W0104
HyperLink
ObjectList
ObjectTree
ProxyButton
ProxyLabel
ProxyComboEntry
ProxyComboBox
ProxyCheckButton
ProxyRadioButton
ProxyEntry
ProxyDateEntry
ProxySpinButton
ProxyTextView
# pylint: enable=W0104


def main(args):
    if len(args) < 2:
        print('ERROR: need a filename')
        return

    b = Gtk.Builder()
    b.add_from_file(args[1])

    for o in b.get_objects():
        if isinstance(o, Gtk.Window):
            o.connect('destroy', Gtk.main_quit)
            o.show()

    Gtk.main()

if __name__ == '__main__':
    main(sys.argv)
