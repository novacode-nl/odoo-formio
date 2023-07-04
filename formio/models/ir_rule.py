# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class IrRule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def _formio_compute_direct_domain(self, model_name, mode="read"):
        """ Compute the direct domain, instead of traversing and
        joining all ir.rule records if not internal user.

        Inspired/copied from ir.rule _compute_domain, but with slight
        modifications."""
        if self.env.user.has_group('base.group_user'):
            # regular domain for internal user (not direct)
            return super()._compute_domain(model_name, mode)
        else:
            eval_context = self._eval_context()
            user_groups = self.env.user.groups_id
            global_domains = []                     # list of domains
            group_domains = []                      # list of domains
            rule = self.sudo()

            if not set(user_groups.ids).intersection(set(rule.groups.ids)):
                return self._compute_domain(model_name, mode)

            # evaluate the domain for the current user
            dom = safe_eval(rule.domain_force, eval_context) if rule.domain_force else []
            dom = expression.normalize_domain(dom)
            if not rule.groups:
                global_domains.append(dom)
            elif rule.groups & user_groups:
                group_domains.append(dom)

            # combine global domains and group domains
            if not group_domains:
                return expression.AND(global_domains)
            return expression.AND(global_domains + [expression.OR(group_domains)])
