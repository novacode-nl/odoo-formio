# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

def migrate(cr, version):
    cr.execute("""
        UPDATE formio_builder
        SET wizard_on_change_page_save_draft = True
        WHERE wizard_on_next_page_save_draft = True
    """)
