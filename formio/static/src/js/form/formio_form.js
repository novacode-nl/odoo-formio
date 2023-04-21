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
        this.language = null;
        this.locales = {};
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
        this.apiUrl = null;
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

    resetParentIFrame() {
        // Ensures (also) the height shall be recomputed
        if ('parentIFrame' in window) {
            parentIFrame.reset();
        }
    }

    loadForm() {
        const self = this;
        let configUrl = self.configUrl;
        const windowParams = new URLSearchParams(window.location.search);
        if (windowParams) {
            configUrl += '?' + windowParams.toString();
        }
        else if (window.parent.location.search) {
            const parentParams = new URLSearchParams(window.parent.location.search);
            if (parentParams) {
                configUrl += '?' + parentParams.toString();
            }
        }
        $.jsonRpc.request(configUrl, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                self.schema = result.schema;
                self.options = result.options;
                self.language = self.options.language;
                self.locales = result.locales;
                self.defaultLocaleShort = self._localeShort(self.language);
                self.params = result.params;
                self.createForm();
            }
        });
    }

    /**
     * onChange handler
     *
     * @param form: The form instance
     * @param changed: The changes that occurred, and the component that triggered the change.
     *   See "componentChange" event:
     *   - instance: The component instance
     *   - component: The component json
     *   - value: The value that was changed
     *   - flags: The flags for the change event loop
     * @param flags: The change loop flags
     * @param modified: Flag to determine if the change was
     *   made by a human interaction, or programatic
     */
    onChange(form, changed, flags, modified) {
        const self = this;
        const hasChanged = typeof changed !== 'undefined' && typeof changed.changed !== 'undefined';
        if (hasChanged) {
            if (changed.changed.component) {
                const component = changed.changed.component;
                const instance = changed.changed.instance;
                if (component.properties.hasOwnProperty('change')) {
                    let apiUrl = self.apiUrl;
                    apiUrl += '/' + 'componentChange' + '/' + component.properties.change;
                    let instanceData = {};
                    if (instance.hasOwnProperty('parent')) {
                        instanceData.parent_component = {
                            'key': instance.parent.component.key,
                            'type': instance.parent.component.type,
                        };
                    }
                    if (instance.hasOwnProperty('path')) {
                        instanceData.path = instance.path;
                    }
                    const data = {
                        'changed': {
                            'component': {
                                'key': component.key,
                                'type': component.type
                            },
                            'instance': instanceData,
                            'value': changed.changed.value,
                        },
                        'form_data': form.data
                    };
                    $.jsonRpc.request(apiUrl, 'call', {'data': data}).then(function(result) {
                        form.submission = {'data': JSON.parse(result)};
                    });
                }
            }
        }
    }

    createForm() {
        const self = this;
        // this does some flatpickr (datetime) locale all over the place.
        if ('language' in self.options && window.flatpickr != undefined) {
            (window).flatpickr.localize((window).flatpickr.l10ns[self.defaultLocaleShort]);
        }
        Formio.setBaseUrl(window.location.href);
        self['options']['hooks'] = {
            attachComponent: (element, instance) => {
                if (instance.component.type == 'datetime') {
                    self._localizeComponent(instance.component, self.language);
                }
            }
        };
        Formio.createForm(document.getElementById('formio_form'), self.schema, self.options).then(function(form) {
            window.setLanguage = function(lang) {
                self.language = lang;
                form.language = lang;
                // component with URL filter: add language
                FormioUtils.eachComponent(form.components, (component) => {
                    let compObj = component.component;
                    if (compObj.hasOwnProperty('data') &&
                        compObj.data.hasOwnProperty('url') && !$.isEmptyObject(compObj.data.url)) {
                        let filterParams = new URLSearchParams(compObj.filter);
                        filterParams.set('language', form.language);
                        compObj.filter = filterParams.toString();
                    }
                });
                // flatpickr (datetime) localization
                if (window.flatpickr != undefined) {
                    const localeShort = self._localeShort(lang);
                    (window).flatpickr.localize((window).flatpickr.l10ns[localeShort]);
                    form.everyComponent((component) => {
                        if (component.type == 'datetime') {
                            self._localizeComponent(component.component, form.language);
                            component.redraw();
                        }
                    });
                }
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
            form.on('change', function(changed, flags, modified) {
                // - changed: The changes that occurred, and the component that triggered the change.
                //   See "componentChange" event:
                //   - instance: The component instance
                //   - component: The component json
                //   - value: The value that was changed
                //   - flags: The flags for the change event loop
                // - flags: The change loop flags
                // - modified: Flag to determine if the change was
                //   made by a human interaction, or programatic
                if (changed.hasOwnProperty('changed')) {
                    self.onChange(form, changed, flags, modified);
                }
            });

            form.on('dataGridAddRow', function(component, row) {
                if (!$.isEmptyObject(self.locales)) {
                    let reloadComponents = [];
                    FormioUtils.eachComponent(component.component.components, (componentObj) => {
                        let localizedComponent = self._localizeComponent(componentObj, self.language);
                        if (localizedComponent) {
                            reloadComponents.push(componentObj);
                        }
                    }, true);
                    if (reloadComponents.length > 0) {
                        const localeShort = self._localeShort(self.language);
                        form.everyComponent((component) => {
                            for (let i=0; i < reloadComponents.length; i++) {
                                let reloadComponent = reloadComponents[i];
                                if (component.type == reloadComponent.type && component.key == reloadComponent.key) {
                                    if (component.component.widget.language !== localeShort) {
                                        component.component.widget.language = localeShort;
                                        component.component.widget.locale = localeShort;
                                        component.redraw();
                                    }
                                }
                            }
                        });
                    }
                }
            });

            // TODO similar to 'dataGridAddRow'
            // form.on('editGridAddRow', function(component, row) {});
            // form.on('rowAdd', function(component, row) {});

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

            // wizard
            form.on('wizardPageSelected', function(submission) {
                self.resetParentIFrame();
            });

            form.on('prevPage', function(submission) {
                self.resetParentIFrame();
            });

            form.on('nextPage', function(submission) {
                self.resetParentIFrame();
                // readOnly check also applies in server endpoint
                const readOnly = 'readOnly' in self.options && self.options['readOnly'] == true;
                if (self.params['wizard_on_next_page_save_draft'] && !readOnly) {
                    const data = {'data': form.data, 'saveDraft': true};
                    if (self.formUuid) {
                        data['form_uuid'] = self.formUuid;
                    }
                    $.jsonRpc.request(self.submitUrl, 'call', data).then(function(submission) {
                        if (typeof(submission) != 'undefined') {
                            // Set properties to instruct the next calls to save (draft) the current form.
                            self.formUuid = submission.form_uuid;
                            self.submitUrl = self.wizardSubmitUrl + self.formUuid + '/submit';
                        }
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

    _localizeComponent(component, language) {
        /** IMPORTANT !
            localization of datetime component (flatpickr widget)
            works since formio.js version 5.0.0-rc.4
        */
        if (component.type == 'datetime') {
            const localeShort = this._localeShort(language);
            component.widget.language = localeShort;
            component.widget.locale = localeShort;
            return true;
        }
        else
        {
            return false;
        }
    }

    _localeShort(language) {
        if (this.locales.hasOwnProperty(language)) {
            return this.locales[language];
        }
        else {
            // not really ok, but could work
            return language.slice(0, 2);
        }
    }
}
