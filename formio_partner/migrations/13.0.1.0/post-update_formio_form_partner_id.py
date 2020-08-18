# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

def migrate(cr, version):
    update_query = """
    UPDATE formio_form
    SET partner_id = base_res_partner_id
    """
    cr.execute(update_query)
