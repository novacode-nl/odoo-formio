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

        // by initForm
        this.builderUuid = null;
        this.formUuid = null;

        // urls
        this.baseUrl = window.location.protocol + '//' + window.location.host;
        this.configUrl = null;
        this.submissionUrl = null;
        this.submitUrl = null;
        this.wizardSubmitUrl = null;
        this.apiUrl = null;
        this.apiValidationUrl = null;
        this.urlParams = new URLSearchParams(window.location.search);

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

    wizardStateChange (form, submission) {
        this.resetParentIFrame();
        // readOnly check also applies in server endpoint
        const readOnly = 'readOnly' in this.options && this.options['readOnly'] == true;
        if (this.params['wizard_on_change_page_save_draft'] && !readOnly) {
            form.beforeSubmit();
            const data = {'data': form.data, 'saveDraft': true};
            if (this.formUuid) {
                data['form_uuid'] = this.formUuid;
            }
            $.jsonRpc.request(this.submitUrl, 'call', data).then(function(submission) {
                if (typeof(submission) != 'undefined') {
                    // Set properties to instruct the next calls to save (draft) the current form.
                    this.formUuid = submission.form_uuid;
                    this.submitUrl = this.wizardSubmitUrl + this.formUuid + '/submit';
                }
            });
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
                self.defaultLocaleShort = self.localeShort(self.language);
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

    /**
     * onBlur handler
     *
     * @param form: The form instance
     * @param instance: The component instance.
     */
    onBlur(form, instance) {
        const self = this;
        if (instance.component) {
            const component = instance.component;
            // const instance = changed.changed.instance;
            if (component.properties.hasOwnProperty('blur')) {
                let apiUrl = self.apiUrl;
                apiUrl += '/' + 'componentChange' + '/' + component.properties.blur;
                let instanceData = {};
                if (instance.hasOwnProperty('parent')) {
                    instanceData.parent_component = {
                        'key': instance.parent.key,
                        'type': instance.parent.type,
                    };
                }
                if (instance.hasOwnProperty('path')) {
                    instanceData.path = instance.path;
                }
                const data = {
                    'changed': {
                        'component': {
                            'key': instance.key,
                            'type': component.type
                         },
                        'instance': instanceData,
                        'value': instance.getValue(),
                    },
                    'form_data': form._data
                };
                $.jsonRpc.request(apiUrl, 'call', {'data': data}).then(function(result) {
                    form.submission = {'data': JSON.parse(result)};
                });
            }
        }
    }

    createForm() {
        const self = this;
        // this does some flatpickr (datetime) locale all over the place.
        if ('language' in self.options && window.flatpickr != undefined) {
            (window).flatpickr.localize((window).flatpickr.l10ns[self.defaultLocaleShort]);
        }

        if (Formio.hasOwnProperty('cdn')) {
	    this.patchCDN();
	    Formio.cdn.setBaseUrl(self.params['cdn_base_url']);
        }

        Formio.setBaseUrl(window.location.href);
        self['options']['hooks'] = {
            attachComponent: (element, instance) => {
                if (instance.component.type == 'datetime') {
                    self.localizeComponent(instance.component, self.language);
                }
            },
            customValidation: (submission, next) => {
                if (self.params.hasOwnProperty('hook_api_validation')
                    && !!self.params['hook_api_validation'])
                {
                    const data = {'data': submission.data, 'lang_ietf_code': self.language};
                    $.jsonRpc.request(self.apiValidationUrl, 'call', data).then(function(errors) {
                        if (!$.isEmptyObject(errors)) {
                            next(errors);
                        }
                        else {
                            next();
                        }
                    });
                }
                else {
                    next();
                }
            }
        };
        Formio.createForm(document.getElementById('formio_form'), self.schema, self.options).then(function(form) {
            let loading = document.getElementById('formio_form_loading');
            let buttons = document.querySelectorAll('.formio_languages button');

            if (loading) {
                loading.style.display = 'none';
            }
            buttons.forEach(function(btn) {
                if (self.language === btn.lang) {
                    btn.classList.add('language_button_active');
                };
            });

            window.setLanguage = function(lang, button) {
                self.language = lang;
                form.language = lang;
                var buttons = document.querySelectorAll('.formio_languages button');
                buttons.forEach(function(btn) {
                    btn.classList.remove('language_button_active');
                });
                button.classList.add('language_button_active');
                // component with URL filter: add language
                FormioUtils.eachComponent(form.components, (component) => {
                    let compObj = component.component;
                    if (self.hasComponentDataURL(compObj)) {
                        let filterParams = new URLSearchParams(compObj.filter);
                        filterParams.set('language', form.language);
                        compObj.filter = filterParams.toString();
                    }
                });
                // flatpickr (datetime) localization
                if (window.flatpickr != undefined) {
                    const localeShort = self.localeShort(lang);
                    (window).flatpickr.localize((window).flatpickr.l10ns[localeShort]);
                    form.everyComponent((component) => {
                        if (component.type == 'datetime') {
                            self.localizeComponent(component.component, form.language);
                            component.redraw();
                        }
                    });
                }
            };

            // Alter the data (Data Source) URL, prefix with Odoo controller endpoint.
            // This also accounts nested components eg inside datagrid, editgrid.
            FormioUtils.eachComponent(form.components, (component) => {
                let compObj = component.component;
                if (self.hasComponentDataURL(compObj)) {
                    compObj.data.url = self.getDataUrl(compObj);
                    let filterParams = new URLSearchParams(compObj.filter);
                    filterParams.set('language', form.language);
                    compObj.filter = filterParams.toString();
                }
            });

            // Events
            form.on('change', function(changed, flags, modified) {
                // A value has been changed within the rendered form
                //
                // @param changed: The changes that occurred, and the component that triggered the change.
                //   See "componentChange" event:
                //   - instance: The component instance
                //   - component: The component json
                //   - value: The value that was changed
                //   - flags: The flags for the change event loop
                // @param flags: The change loop flags
                // @param modified: Flag to determine if the change was
                //   made by a human interaction, or programatic
                if (changed.hasOwnProperty('changed')) {
                    self.onChange(form, changed, flags, modified);
                }
            });

            form.on('blur', function(instance) {
                // Triggered when an input component has been blurred
                //
                // @param instance: The component instance.
                if (instance) {
                    self.onBlur(form, instance);
                }
            });

            form.on('dataGridAddRow', function(component, row) {
                if (!$.isEmptyObject(self.locales)) {
                    let reloadComponents = [];
                    FormioUtils.eachComponent(component.component.components, (componentObj) => {
                        let localizedComponent = self.localizeComponent(componentObj, self.language);
                        if (localizedComponent) {
                            reloadComponents.push(componentObj);
                        }
                    }, true);
                    if (reloadComponents.length > 0) {
                        const localeShort = self.localeShort(self.language);
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
                // readOnly check also applies in server endpoint
                const readOnly = 'readOnly' in self.options && self.options['readOnly'] == true;
                if (self.params['wizard_on_change_page_save_draft'] && !readOnly) {
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

            form.on('prevPage', function(submission) {
                self.resetParentIFrame();
                // readOnly check also applies in server endpoint
                const readOnly = 'readOnly' in self.options && self.options['readOnly'] == true;
                if (self.params['wizard_on_change_page_save_draft'] && !readOnly) {
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

            form.on('nextPage', function(submission) {
                self.resetParentIFrame();
                // readOnly check also applies in server endpoint
                const readOnly = 'readOnly' in self.options && self.options['readOnly'] == true;
                if (self.params['wizard_on_change_page_save_draft'] && !readOnly) {
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

    patchCDN() {
	// CDN class is not exported, so patch it here because
	// ckeditor's URLs are somewhat nonstandard.
        //
        // The patch implements a fallback for formio.js version
        // <= 4.14.12, where CDN.buildUrl is not implemented, to
        // patch CDN.updateUrls.
        //
	// When using an external CDN, we must also avoid loading the customized
	// version of flatpickr, instead relying on the default version.
        if (Formio.cdn.buildUrl !== undefined && typeof(Formio.cdn.buildUrl === 'function')) {
            const oldBuildUrl = Formio.cdn.buildUrl.bind(Formio.cdn);
            Formio.cdn.buildUrl = function(cdnUrl, lib, version) {
                if (lib == 'ckeditor') {
                    if (version == '19.0.0') {
                        // Somehow 19.0.0 is missing?!
                        version = '19.0.1';
                    }
                    return `${cdnUrl}/${lib}5/${version}`;
                } else if (lib == 'flatpickr-formio') {
                    return oldBuildUrl(cdnUrl, 'flatpickr', this.libs['flatpickr']);
                } else {
                    return oldBuildUrl(cdnUrl, lib, version);
                }
            };
        } else {
            const oldUpdateUrls = Formio.cdn.updateUrls.bind(Formio.cdn);
            Formio.cdn.updateUrls = function() {
                for (const lib in this.libs) {
                    let version = this.libs[lib];
                    if (version === '') {
                        this[lib] = `${this.baseUrl}/${lib}`;
                    }
                    else if (lib == 'ckeditor') {
                        if (version == '19.0.0') {
                            // Somehow 19.0.0 is missing?!
                            version = '19.0.1';
                        }
                        this[lib] = `${this.baseUrl}/${lib}5/${version}`;
                    } else if (lib == 'flatpickr-formio') {
                        const flatpickr_version = this.libs['flatpickr'];
                        this[lib] = `${this.baseUrl}/flatpickr/${flatpickr_version}`;
                    } else {
                        this[lib] = `${this.baseUrl}/${lib}/${this.libs[lib]}`;
                    }
                }
            };
        }
    }

    patchRequireLibary() {
        // Formio requireLibrary method is not exported, so patch it
        // here because the standard CDNs use a different flatpickr
        // naming and src URLs.
        const oldRequireLibrary= Formio.requireLibrary.bind(Formio);
        Formio.requireLibrary = function(name, property, src, polling) {
            const src_is_string = typeof(src) === 'string';
            if (src_is_string
                && src.includes('flatpickr')
                && src.includes('l10n'))
            {
                ////////////////////////////////////////////////////
                // HACK - SPECIAL CASE for flatpickr l10n (locales).
                ////////////////////////////////////////////////////
                // EXAMPLE of rewriting:
                // name: flatpickr-nl-NL
                // nameLang: nl-NL
                // nameShort: nl
                let nameLang = name.replaceAll('flatpickr-', '');
                // nameShort
                let nameShort = nameLang;
                if (nameLang !== 'default') {
                    nameShort = nameLang.substring(0, 2);
                }
                if (nameShort == 'en') {
                    nameShort = 'default';
                }
                // property
                property = property.replaceAll('flatpickr-', '');
                if (property !== 'default') {
                    property = property.substring(0, 2);
                }
                if (property == 'en') {
                    property = 'default';
                }
                // src
                src = src.replaceAll('flatpickr-', '').replaceAll('.js', '.min.js');
                src = src.replaceAll(nameLang, nameShort);
                return oldRequireLibrary(nameShort, property, src, polling);
            }
            else if (src_is_string
                     && name != 'flatpickr-css'
                     && name.includes('flatpickr-'))
            {
                name = name.replaceAll('flatpickr-', '');
                property = property.replaceAll('flatpickr-', '');
                src = src.replaceAll('flatpickr-', '').replaceAll('.js', '.min.js');
                return oldRequireLibrary(name, property, src, polling);
            }
            else {
                return oldRequireLibrary(name, property, src, polling);
            }
        };
    }

    hasComponentDataURL(component) {
        return component
            && component.hasOwnProperty('data')
            && component.data.hasOwnProperty('url')
            && !$.isEmptyObject(component.data.url);
    }

    localizeComponent(component, language) {
        /** IMPORTANT !
            localization of datetime component (flatpickr widget)
            works since formio.js version 5.0.0-rc.4
        */
        if (component.type == 'datetime') {
            const localeShort = this.localeShort(language);
            component.widget.language = localeShort;
            component.widget.locale = localeShort;
            return true;
        }
        else
        {
            return false;
        }
    }

    localeShort(language) {
        if (this.locales.hasOwnProperty(language)) {
            return this.locales[language];
        }
        else {
            // not really ok, but could work
            return language.slice(0, 2);
        }
    }
}
