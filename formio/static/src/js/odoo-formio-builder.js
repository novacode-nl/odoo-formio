// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

odoo.define('formio.Builder', ['web.ajax'], function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function() {
        var builder_id = document.getElementById('builder_id').value,
            schema_url = '/formio/builder/schema/' + builder_id,
            save_url = '/formio/builder/save/' + builder_id,
            schema = {};
        
        ajax.jsonRpc(schema_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                schema = JSON.parse(result); // Form JSON schema
            }

            // Render the Builder (with JSON schema).
            Formio.builder(document.getElementById('formio_builder'), schema).then(function(builder) {
                builder.on('change', function(res) {
                    console.log('[Form.io] Saving Builder...');
                    ajax.jsonRpc(save_url, 'call', {
                        'builder_id': builder_id,
                        'schema': builder.schema
                    }).then(function() {
                        console.log('[Form.io] Builder sucessfully saved.');
                    });
                });
            });
        });
    });
});
