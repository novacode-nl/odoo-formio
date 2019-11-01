# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

def migrate(cr, version):
    update_query = """
    UPDATE formio_builder
    SET formio_res_model_id = (SELECT rm.id FROM formio_res_model AS rm WHERE rm.ir_model_id = res_model_id)
    """
    cr.execute(update_query)
