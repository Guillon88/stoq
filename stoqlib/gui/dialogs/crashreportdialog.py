# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2011 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##
""" Crash report dialog """

import gtk

from kiwi.ui.dialogs import HIGAlertDialog

from stoqlib.gui.base.dialogs import get_current_toplevel
from stoqlib.lib.crashreport import ReportSubmitter
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext

_N_TRIES = 3


class CrashReportDialog(object):
    def __init__(self, parent, params):
        self._params = params
        self._parent = parent
        self._report_submitter = ReportSubmitter(params)
        self._report_submitter.connect('submitted',
                                       self._on_report__submitted)
        self._report_submitter.connect('failed',
                                       self._on_report__failed)
        self._create_dialog()

    def _create_dialog(self):
        self._dialog = HIGAlertDialog(parent=self._parent,
                                      flags=gtk.DIALOG_MODAL,
                                      type=gtk.MESSAGE_WARNING)

        self._dialog.set_primary(
            _('We\'r sorry to inform you that an error occurred while '
              'running %s. Please help us improving Stoq by sending a '
              'automatically generated report about the incident.\n'
              'Click on details to see the report text.') % (
            self._params['app-name'], ), bold=False)

        sw = gtk.ScrolledWindow()
        view = gtk.TextView()
        view.set_size_request(500, 350)
        view.get_buffer().set_text(self._report_submitter.report)
        sw.add(view)
        view.show()
        self._dialog.set_details_widget(sw)
        self._no_button = self._dialog.add_button(_('No thanks'),
                                                  gtk.RESPONSE_NO)
        self._yes_button = self._dialog.add_button(_('Send report'),
                                                   gtk.RESPONSE_YES)

    def _finish(self):
        self._yes_button.set_label(_("Close"))
        self._yes_button.set_sensitive(True)

    def _show_report(self, data):
        label = gtk.LinkButton(
            data['report-url'],
            _("Report %s successfully opened") % data['report'])
        self._dialog.vbox.pack_start(label)
        label.show()
        self._finish()

    def _show_error(self):
        label = gtk.Label(_("Failed to submit bugreport"))
        self._dialog.vbox.pack_start(label)
        label.show()
        self._finish()

    def run(self):
        response = self._dialog.run()
        if response == gtk.RESPONSE_NO:
            return False

        self._no_button.hide()
        self._yes_button.set_sensitive(False)
        self._yes_button.set_label(_('Sending...'))
        self._parent.destroy()

        self._report_submitter.submit()
        self._dialog.run()
        return True

    def _on_report__failed(self, response, args):
        self._show_error()

    def _on_report__submitted(self, response, data):
        self._show_report(data)


def show_dialog(params, interactive=True):
    """Show a crash report dialog
    @param: dictionary of parameters
    """
    parent = get_current_toplevel()
    crd = CrashReportDialog(parent, params)
    crd.run()
