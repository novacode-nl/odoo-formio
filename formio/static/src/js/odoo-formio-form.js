// Copyright 2018 Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

odoo.define('formio.Form', ['web.ajax'], function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function() {
        var uuid = document.getElementById('form_uuid').value,
            base_url = window.location.protocol + '//' + window.location.host,
            schema_url = '/formio/form/schema/' + uuid,
            submission_url = '/formio/form/submission/' + uuid,
            submit_url = '/formio/form/submit/' + uuid,
            schema = {};

        ajax.jsonRpc(schema_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                schema = JSON.parse(result);

                var hooks = {
                    'addComponent': function(container, comp, parent) {
                        if (comp.component.hasOwnProperty('data') && comp.component.data.hasOwnProperty('url') &&
                            !$.isEmptyObject(comp.component.data.url)) {
                            comp.component.data.url = base_url.concat(comp.component.data.url, '/', uuid);
                        }
                        return container;
                    }
                };

                //formio.icons = 'fontawesome';
                Formio.createForm(document.getElementById('formio_form'), schema, {hooks: hooks}).then(function(form) {
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
            }
        });
    });
});
