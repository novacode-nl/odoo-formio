# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

def migrate(cr, version):
    """
    ir.model.fields.selection
    formio.selection__formio_extra_asset__target__prepend
    """
    cr.execute("""
        DELETE FROM ir_model_fields_selection
        WHERE field_id IN (
            SELECT id
            FROM
              ir_model_fields
            WHERE
              model = 'formio.extra.asset'
        )
    """)
