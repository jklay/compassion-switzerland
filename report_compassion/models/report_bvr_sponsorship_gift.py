# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################

import logging


from openerp import api, models

logger = logging.getLogger(__name__)


class BvrSponsorshipGift(models.Model):
    """
    Model used for preparing data for the bvr report. It can either
    generate 3bvr report or single bvr report.
    """
    _name = 'report.report_compassion.bvr_gift_sponsorship'

    def _get_report(self):
        return self.env['report']._get_report_from_name(
            'report_compassion.bvr_gift_sponsorship')

    def _get_default_data(self):
        """
        If no data is given for the report, use default values.
        :return: default mandatory data for the bvr report.
        """
        return {
            'doc_ids': self._ids,
            'product_ids': self.env[
                'recurring.contract'].get_sponsorship_gift_products().ids
        }

    @api.multi
    def render_html(self, data=None):
        """
        Construct the data for printing Payment Slips.
        :param data: data collected from the print wizard.
        :return: html rendered report
        """
        report = self._get_report()
        final_data = self._get_default_data()
        if data:
            final_data.update(data)

        final_data.update({
            'doc_model': report.model,  # recurring.contract
            'docs': self.env[report.model].browse(final_data['doc_ids']),
            'products': self.env['product.product'].browse(
                final_data['product_ids'])
        })
        return self.env['report'].render(report.report_name, final_data)


class ThreeBvrGiftSponsorship(models.Model):
    _inherit = 'report.report_compassion.bvr_gift_sponsorship'
    _name = 'report.report_compassion.3bvr_gift_sponsorship'

    def _get_report(self):
        return self.env['report']._get_report_from_name(
            'report_compassion.3bvr_gift_sponsorship')

    @api.multi
    def render_html(self, data=None):
        """ Include setting for telling 3bvr paper has offset between
        payment slips.
        """
        if data is None:
            data = dict()
        data['offset'] = 1
        return super(ThreeBvrGiftSponsorship, self).render_html(data)
