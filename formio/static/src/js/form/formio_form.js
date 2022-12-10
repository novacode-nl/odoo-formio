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
        this.params = {}; // extra params from Odoo backend

        this.baseUrl = window.location.protocol + '//' + window.location.host;
        this.urlParams = new URLSearchParams(window.location.search);

        // by initForm
        this.builderUuid = null;
        this.formUuid = null;
        this.configUrl = null;
        this.submissionUrl = null;
        this.submitUrl = null;
        this.wizardSubmitUrl = null;
    }

    willStart() {
        this.initForm();
    }

    mounted() {
        this.loadForm();
    }

    initForm() {
        // Implemented in specific (*_app.js) classes.
    }

    submitDone(submission) {
        // Implemented in specific (*_app.js) classes.
    }

    getDataUrl(compObj) {
        // Possibly overridden in specific (*_app.js) classes.
        return '/formio/form/', self.formUuid, compObj.data.url;
    }

    loadForm() {
        const self = this;

        $.jsonRpc.request(self.configUrl, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                self.schema = result.schema;
                self.options = result.options;
                self.params = result.params;
                self.createForm();
            }
        });
    }

    createForm() {
        const self = this;

        Formio.setBaseUrl(window.location.href);
        Formio.createForm(document.getElementById('formio_form'), self.schema, self.options).then(function(form) {
            // Language
            if ('language' in self.options) {
                form.language = self.options['language'];
            }
            window.setLanguage = function(lang) {
                form.language = lang;
                FormioUtils.eachComponent(form.components, (component) => {
                    let compObj = component.component;
                    if (compObj.hasOwnProperty('data') &&
                        compObj.data.hasOwnProperty('url') && !$.isEmptyObject(compObj.data.url)) {
                        let filterParams = new URLSearchParams(compObj.filter);
                        filterParams.set('language', form.language);
                        compObj.filter = filterParams.toString();
                    }
                });
            };

            // Alter the data (Data Source) URL, prefix with Odoo controller endpoint.
            // This also accounts nested components eg inside datagrid, editgrid.
            FormioUtils.eachComponent(form.components, (component) => {
                let compObj = component.component;
                if (compObj.hasOwnProperty('data') &&
                    compObj.data.hasOwnProperty('url') && !$.isEmptyObject(compObj.data.url)) {
                    compObj.data.url = self.getDataUrl(compObj);
                    let filterParams = new URLSearchParams(compObj.filter);
                    filterParams.set('language', form.language);
                    compObj.filter = filterParams.toString();
                }
            });

            // Events
            form.on('submit', function(submission) {
                const data = {'data': submission.data};
                if (self.formUuid) {
                    data['form_uuid'] = self.formUuid;
                }
                $.jsonRpc.request(self.submitUrl, 'call', data).then(function() {
                    form.emit('submitDone', submission);
                });
            });

            form.on('submitDone', function(submission) {
                self.submitDone(submission);
            });

            // wizard nextPage
            form.on('nextPage', function() {
                // readOnly check also applies in server endpoint
                const readOnly = 'readOnly' in self.options && self.options['readOnly'] == true;
                if (self.params['wizard_on_next_page_save_draft'] && !readOnly) {
                    const data = {'data': form.data, 'saveDraft': true};
                    if (self.formUuid) {
                        data['form_uuid'] = self.formUuid;
                    }
                    $.jsonRpc.request(self.submitUrl, 'call', data).then(function(submission) {
                        // Set properties to instruct the next calls to save (draft) the current form.
                        self.formUuid = submission.form_uuid;
                        self.submitUrl = self.wizardSubmitUrl + self.formUuid + '/submit';
                    });
                }
            });

            // Set the Submission (data)
            // https://github.com/formio/formio.js/wiki/Form-Renderer#setting-the-submission
            if (self.submissionUrl) {
                let submissionUrl = self.submissionUrl;
                if (self.params.hasOwnProperty('submission_url_add_query_params_from')) {
                    if (self.params['submission_url_add_query_params_from'] == 'window' && window.location.search) {
                        const params = new URLSearchParams(window.location.search);
                        submissionUrl += '?' + params.toString();
                    }
                    else if (self.params['submission_url_add_query_params_from'] == 'window.parent' && window.parent.location.search) {
                        const params = new URLSearchParams(window.parent.location.search);
                        submissionUrl += '?' + params.toString();
                    }
                }
                $.jsonRpc.request(submissionUrl, 'call', {}).then(function(result) {
                    if (!$.isEmptyObject(result)) {
                        form.submission = {'data': JSON.parse(result)};
                    }
                });
            }
        });
    }
}
