# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

def migrate(cr, version):
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE model = 'formio.version'
    """)
