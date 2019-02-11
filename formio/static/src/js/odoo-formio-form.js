// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

odoo.define('formio.Form', ['web.ajax'], function (require) {
    "use strict";

    // TODO Get rid of callbacks and refactor in a classy way.
    // This should init the Form with schema_url and options_url.
    var ajax = require('web.ajax');

    $(document).ready(function() {
        var uuid = document.getElementById('form_uuid').value,
            base_url = window.location.protocol + '//' + window.location.host,
            schema_url = '/formio/form/schema/' + uuid,
            options_url = '/formio/form/options/' + uuid,
            submission_url = '/formio/form/submission/' + uuid,
            submit_url = '/formio/form/submit/' + uuid,
            schema = {},
            options = {};

        ajax.jsonRpc(schema_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                schema = JSON.parse(result);

                ajax.jsonRpc(options_url, 'call', {}).then(function(_options) {
                    var options = JSON.parse(_options);
                    var hooks = {
                        'addComponent': function(container, comp, parent) {
                            if (comp.component.hasOwnProperty('data') && comp.component.data.hasOwnProperty('url') &&
                                !$.isEmptyObject(comp.component.data.url)) {
                                comp.component.data.url = base_url.concat(comp.component.data.url, '/', uuid);
                            }
                            return container;
                        }
                    };
                    options['hooks'] = hooks;

                    Formio.createForm(document.getElementById('formio_form'), schema, options).then(function(form) {
                        if ('language' in options) {
                            form.language = options['language'];
                        }
                        // Events
                        form.on('submit', function(submission) {
                            ajax.jsonRpc(submit_url, 'call', {
                                'uuid': uuid,
                                'data': submission.data
                            }).then(function() {
                                form.emit('submitDone', submission);
                            });
                        });
                        // Set the Submission (data)
                        // https://github.com/formio/formio.js/wiki/Form-Renderer#setting-the-submission
                        ajax.jsonRpc(submission_url, 'call', {}).then(function(result) {
                            if (!$.isEmptyObject(result)) {
                                form.submission = {'data': JSON.parse(result)};
                            }
                        });
                    });
                });
            }
        });
    });
});
