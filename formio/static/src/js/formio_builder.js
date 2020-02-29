// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

$(document).ready(function() {
    var builder_id = document.getElementById('builder_id').value,
        schema_url = '/formio/builder/schema/' + builder_id,
        options_url = '/formio/builder/options/' + builder_id,
        save_url = '/formio/builder/save/' + builder_id,
        schema = {};

    $.jsonRpc.request(options_url, 'call', {}).then(function(_options) {
        var options = JSON.parse(_options);

        $.jsonRpc.request(schema_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                schema = JSON.parse(result); // Form JSON schema
            }

            // Render the Builder (with JSON schema).
            Formio.builder(document.getElementById('formio_builder'), schema).then(function(builder) {
                builder.on('change', function(res) {
                    if ('readOnly' in options && options['readOnly'] == true) {
                        alert("This Form Builder is readonly. It's state is either Current or Obsolete. Refresh the page again.");
                        return;
                    }
                    else {
                        console.log('[Form.io] Saving Builder...');
                        $.jsonRpc.request(save_url, 'call', {
                            'builder_id': builder_id,
                            'schema': builder.schema
                        }).then(function() {
                            console.log('[Form.io] Builder sucessfully saved.');
                        });
                    }
                });
            });
        });
    });
});
