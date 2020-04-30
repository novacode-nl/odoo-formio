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
                    init_resizer();

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

    var init_resizer = function() {
        /* HACK
           This is a hacky workaround regarding issue https://github.com/novacode-nl/odoo-formio/issues/20
           The iframeResizer library doen't get triggered upon using the component-types below.

           TODO
           .formio-component-day (months dropdown) doesn't trigger.
        */
        var initial_height = $(document.getElementById('formio_form')).height();
        var observer = new MutationObserver(function(mutations) {
            var new_height = false;
            mutations.forEach(function(mutation) {
                if ($(mutation.target).hasClass('is-open') || $(mutation.target).hasClass('active')) {
                    // Classes used in compoenents (as far as I know):
                    // - is-open: select components
                    // - active: datetime components
                    if (new_height != initial_height) {
                        // Update height
                        if ($(mutation.target).parents('.formio-component-select').length) {
                            new_height = initial_height + 200;
                            $('.formio_form_embed_container').height(new_height);
                        } else if ($(mutation.target).parents('.formio-component-datetime').length) {
                            new_height = initial_height + 300;
                            $('.formio_form_embed_container').height(new_height);
                        } else {
                            $('.formio_form_embed_container').height(initial_height);
                        }
                        console.log('Updated #formio_form height to fix expandbles (dropdowns) positioning.');
                    }
                    else {
                        $(document.getElementById('formio_form')).height(initial_height);
                    }
                }
            });
        });

        // Such last 3 component-types on form cause issues.
        var last_n = -3;
        var components = $("#formio_form .formio-component-select, #formio_form .formio-component-datetime, #formio_form .formio-component-day [ref='month']");
        $.each(components.slice(-3), function(i, el) {
            observer.observe(el, {
                attributes: true,
                attributeFilter: ["class"],
                subtree: true
            });
        });
    };
});
