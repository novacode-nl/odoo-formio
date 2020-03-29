// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

$(document).ready(function() {
    // TODO Get rid of callbacks and refactor in a classy way.
    // Do init the Form object with schema_url and options_url.
    var uuid = document.getElementById('form_uuid').value,
        base_url = window.location.protocol + '//' + window.location.host,
        formio_uuid = '/formio/form/' + uuid,
        schema_url = formio_uuid + '/schema/',
        options_url = formio_uuid + '/options/',
        submission_url = formio_uuid + '/submission/',
        submit_url = formio_uuid + '/submit/',
        schema = {},
        options = {};

    $.jsonRpc.request(schema_url, 'call', {}).then(function(result) {
        if (!$.isEmptyObject(result)) {
            schema = JSON.parse(result);

            $.jsonRpc.request(options_url, 'call', {}).then(function(_options) {
                var options = JSON.parse(_options);
                var hooks = {
                    'addComponent': function(container, comp, parent) {
                        if (comp.hasOwnProperty('component') && comp.component.hasOwnProperty('data') &&
                            comp.component.data.hasOwnProperty('url') && !$.isEmptyObject(comp.component.data.url)) {
                            comp.component.data.url = base_url.concat(comp.component.data.url, '/', uuid);
                        }
                        return container;
                    }
                };
                options['hooks'] = hooks;

                Formio.createForm(document.getElementById('formio_form'), schema, options).then(function(form) {
                    // Language
                    if ('language' in options) {
                        form.language = options['language'];
                    }
                    window.setLanguage = function(lang) {
                        form.language = lang;
                    };
                    
                    // Events
                    form.on('submit', function(submission) {
                        $.jsonRpc.request(submit_url, 'call', {
                            'uuid': uuid,
                            'data': submission.data
                        }).then(function() {
                            form.emit('submitDone', submission);
                        });
                    });
                    form.on('submitDone', function(submission) {
                        if (submission.state == 'submitted') {
                            window.parent.postMessage('formioSubmitDone', base_url);
                        }
                        window.location.reload();
                    });
                    // Set the Submission (data)
                    // https://github.com/formio/formio.js/wiki/Form-Renderer#setting-the-submission
                    $.jsonRpc.request(submission_url, 'call', {}).then(function(result) {
                        if (!$.isEmptyObject(result)) {
                            form.submission = {'data': JSON.parse(result)};
                        }
                    });
                });
            });
        }
    });
});
