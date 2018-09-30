odoo.define('formio.Builder', ['web.ajax'], function (require) {
    "use strict";

    var ajax = require('web.ajax');

    window.onload = function() {
        var builder_id = document.getElementById('builder_id').value,
            schema_url = '/formio/builder/schema/' + builder_id,
            post_url = '/formio/builder/post/' + builder_id;
        
        ajax.jsonRpc(schema_url, 'call', {}).then(function(result) {
            var schema = JSON.parse(result); // Form JSON schema
            // Render the Builder (with JSON schema).
            Formio.builder(document.getElementById('formio_builder'), schema).then(function(builder) {
                builder.on('saveComponent', function(component) {
                    return ajax.jsonRpc(post_url, 'call', {
                        'builder_id': builder_id,
                        'schema': builder.schema
                    }).then(function (result) {
                        alert('Done');
                        return 'Done';
                    });
                });
                builder.on('deleteComponent', function(component) {
                    if (!comp.isNew) {
                        // Store in Odoo
                    }
                });
            });
        });
    };

});
