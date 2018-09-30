odoo.define('formio.Builder', ['web.ajax'], function (require) {
    "use strict";

    var ajax = require('web.ajax');

    window.onload = function() {
        var builder_id = document.getElementById('builder_id').value,
            schema_url = '/formio/builder/schema/' + builder_id,
            post_url = '/formio/builder/post/' + builder_id,
            schema = {};
        
        ajax.jsonRpc(schema_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                schema = JSON.parse(result); // Form JSON schema
            }

            // Render the Builder (with JSON schema).
            Formio.builder(document.getElementById('formio_builder'), schema).then(function(builder) {
                builder.on('saveComponent', function(component) {
                    ajax.jsonRpc(post_url, 'call', {
                        'builder_id': builder_id,
                        'schema': builder.schema
                    }).then(function (result) {
                        console.log(result);
                        alert('saved component');
                    });
                });
                builder.on('deleteComponent', function(component) {
                    // TODO Update the builder.schema - Prevent data loss!
                    // Instead building a new_schema['components'] ...
                    // change the present builder.schema.components (by slice()).
                    var new_schema = {'components': []};
                    for (var i=0; i < builder.schema.components.length; i++) {
                        // Check component deleted by key.
                        if (builder.schema.components[i].key != component.key) {
                            new_schema['components'].push(builder.schema.components[i]);
                        }
                    }
                    ajax.jsonRpc(post_url, 'call', {
                        'builder_id': builder_id,
                        'schema': new_schema
                    }).then(function (result) {
                        alert('deleted component');
                    });
                });
            });
        });
    };

});
