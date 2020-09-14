// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

const { Component } = owl;
const { xml } = owl.tags;
const { whenReady } = owl.utils;
const { useState } = owl.hooks;

const actions = {};

const initialState = {
    auth: [],
};

export class OdooFormioForm extends Component {

    constructor(parent, props) {
        super(parent, props);

        this.schema = {};
        this.options = {};
        this.base_url = window.location.protocol + '//' + window.location.host;

        // by initForm
        this.builder_uuid = null;
        this.form_uuid = null;
        this.config_url = null;
        this.submission_url = null;
        this.submit_url = null;
    }

    willStart() {
        this.initForm();
    }

    mounted() {
        this.loadForm();
    }

    initForm() {
        // Implemented in specific (app) class, e.g:
        // - backend_app.js
        // - public_app.js
        // - public_create_app.js
    }

    loadForm() {
        const self = this;

        $.jsonRpc.request(self.config_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                self.schema = result.schema;
                self.options = result.options;
                self.createForm();
            }
        });
    }

    createForm() {
        const self = this;

        // Maybe avoid URL (check) on self.form_uuid
        if (self.form_uuid) {
            const hooks = {
                'addComponent': function(component, comp, parent) {
                    if (component.hasOwnProperty('data') &&
                        component.data.hasOwnProperty('url') && !$.isEmptyObject(component.data.url)) {
                        component.data.url = self.base_url.concat('/formio/form', component.data.url, '/', self.form_uuid);
                    }
                    return component;
                }
            };
            self.options['hooks'] = hooks;
        }

        Formio.createForm(document.getElementById('formio_form'), self.schema, self.options).then(function(form) {
            // Language
            if ('language' in self.options) {
                form.language = self.options['language'];
            }
            window.setLanguage = function(lang) {
                form.language = lang;
            };

            // Events
            form.on('submit', function(submission) {
                const data = {'data': submission.data};
                if (self.form_uuid) {
                    data['form_uuid'] = self.form_uuid;
                }
                $.jsonRpc.request(self.submit_url, 'call', data).then(function() {
                    form.emit('submitDone', submission);
                });
            });
            form.on('submitDone', function(submission) {
                if (submission.state == 'submitted') {
                    window.parent.postMessage('formioSubmitDone', self.base_url);
                }
                setTimeout(function() {
                    window.location.reload();
                }, 500);
            });

            // Set the Submission (data)
            // https://github.com/formio/formio.js/wiki/Form-Renderer#setting-the-submission
            if (self.submission_url) {
                $.jsonRpc.request(self.submission_url, 'call', {}).then(function(result) {
                    if (!$.isEmptyObject(result)) {
                    form.submission = {'data': JSON.parse(result)};
                    }
                });
            }
        });
    }
}
