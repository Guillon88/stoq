# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2013 Async Open Source <http://www.async.com.br>
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
## GNU General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

from stoqlib.reporting.test.reporttest import ReportTest
from stoqlib.lib.dateutils import localdate

from ..opticalreport import OpticalWorkOrderReceiptReport
from .test_optical_domain import OpticalDomainTest


class OpticalReportTest(ReportTest, OpticalDomainTest):

    def test_optical_report(self):
        opt_wo = self.create_optical_work_order()
        wo = opt_wo.work_order
        wo.identifier = 12345
        wo.client = self.create_client()
        sale = self.create_sale()
        sale.identifier = 23456
        sale.open_date = localdate(2012, 1, 1)
        sale.client = self.create_client()
        sale.salesperson = self.create_sales_person()
        wo.sale = sale
        self._diff_expected(OpticalWorkOrderReceiptReport,
                            'optical-work-order-receipt-report',
                            [opt_wo.work_order])