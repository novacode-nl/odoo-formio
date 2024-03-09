// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

// use global owl
// can't import from "@odoo/owl", because not an @odoo-module
const { Component, mount, onMounted, whenReady, xml } = owl;

function app() {
    class App extends Component {
        static template = xml`<div id="formio_builder"></div>`;

        setup() {
            super.setup();
            this.configUrl = null;
            onMounted(() => {
                this.loadBuilder();
            });
        }

        loadBuilder() {
            const self = this;
            self.builderId = document.getElementById('builder_id').value;
            self.configUrl = '/formio/builder/' + self.builderId + '/config';
            self.saveUrl = '/formio/builder/' + self.builderId + '/save';
            self.schema = {};
            self.options = {};
            this.language = null;
            this.locales = {};
            self.params = {};
            self.csrfToken = null;

            // init some builder state
            self.isDirty = false;
            self.cancelComponent = false;

            self.getData(self.configUrl, {}).then(function(res) {
                if (!$.isEmptyObject(res)) {
                    self.schema = res.schema;
                    self.options = res.options;
                    self.params = res.params;
                    self.locales = res.locales;
                    self.csrfToken = res.csrf_token;

                    if ('autoSave' in self.params && self.params['autoSave'] == true) {
                        self.autoSave = true;
                    }
                    else {
                        self.autoSave = false;
                    }

                    if ('readOnly' in self.params && self.params['readOnly'] == true) {
                        self.isReadOnly = true;
                    }
                    else {
                        self.isReadOnly = false;
                    }
                    // TODO language translations and localisations (flatpickr issues)
                    // self.language = self.options.language;
                    // self.defaultLocaleShort = self.localeShort(self.language);
                    //
                    // TODO change this hack, which (maybe) is a silly
                    // workaround when Formbuilder object is not ready.
                    // Issue reported: https://github.com/novacode-nl/odoo-formio/issues/128
                    setTimeout(function() {self.createBuilder();}, 100);
                }
            });
        }

        createBuilder() {
            const self = this;

            this.patchRequireLibary();
            if (Formio.hasOwnProperty('cdn')) {
                this.patchCDN();
                Formio.cdn.setBaseUrl(self.params['cdn_base_url']);
            }

            let builder = new Formio.FormBuilder(document.getElementById('formio_builder'), self.schema, self.options);
            let loading = document.getElementById('formio_builder_loading');
            let buttons = document.querySelectorAll('.formio_languages button');

            loading.style.display = 'none';
            buttons.forEach(function(btn) {
                if (self.options.language === btn.lang) {
                    btn.classList.add('language_button_active');
                };
            });

            builder.instance.ready.then(function() {
                if ('language' in self.options) {
                    builder.language = self.options['language'];
                    // builder.instance.webform.language = self.options['language'];
                    if (window.flatpickr != undefined) {
                        const localeShort = self.localeShort(builder.language);
                        (window).flatpickr.localize((window).flatpickr.l10ns[localeShort]);
                        FormioUtils.eachComponent(builder._form.components, (component) => {
                            if (component.type == 'datetime') {
                                self.localizeComponent(component, builder.language);
                            }
                        });
                    }
                    builder.instance.redraw();
                }
                window.setLanguage = function(lang, button) {
                    builder.instance.webform.language = lang;
                    let buttons = document.querySelectorAll('.formio_languages button');
                    buttons.forEach(function(btn) {
                        btn.classList.remove('language_button_active');
                    });
                    button.classList.add('language_button_active');
                    FormioUtils.eachComponent(builder._form.components, (component) => {
                        if (component.type == 'datetime') {
                            self.localizeComponent(component, lang);
                        }
                    });
                    builder.instance.redraw();
                };
                window.saveFormBuilder = function(button) {
                    if (!self.autoSave) {
                        console.log('[Forms] Saving Builder...');
                        const builder_obj = builder.instance;
                        self.postData(self.saveUrl, {
                            'builder_id': self.builderId,
                            'schema': builder._form
                        }).then(function() {
                            self.hideSaveBuilder();
                            console.log('[Forms] Builder sucessfully saved.');
                        });
                    }
                };
            });

            builder.instance.on('change', function(res) {
                if (! res.hasOwnProperty('components')) {
                    return;
                }
                else if (self.isReadOnly) {
                    alert("WARNING: Nothing is saved!\nThis Form Builder is readonly (probably locked).\nRefresh the page and try again.");
                    return;
                }
                else {
                    if (self.autoSave) {
                        console.log('[Forms] Auto-saving Builder...');
                        self.postData(self.saveUrl, {
                            'schema': builder._form
                        }).then(function() {
                            console.log('[Forms] Builder sucessfully auto-saved.');
                        });
                    } else {
                        self.isDirty = true;
                        self.showSaveBuilder();
                    }
                }
            });

            builder.instance.on('saveComponent', function(schema) {
                if (!self.autoSave) {
                    self.isDirty = true;
                    self.showSaveBuilder();
                }
            });

            builder.instance.on('cancelComponent', function(component) {
                if (!self.autoSave) {
                    // Hack to suppress removeComponent, which propagates as a save.
                    self.cancelComponent = true;
                }
                if (!self.autoSave && !self.isDirty) {
                    self.hideSaveBuilder();
                }
            });

            builder.instance.on('removeComponent', function(component, schema, path, index) {
                if (!self.autoSave) {
                    self.isDirty = true;
                    if (!self.cancelComponent) {
                        self.showSaveBuilder();
                    } else {
                        // Re-initialize the cancelComponent hack.
                        self.cancelComponent = false;
                    }
                }
            });
        }

        showSaveBuilder() {
            if (!this.isReadOnly) {
                let saveButtons = document.querySelectorAll('.formio_save');
                saveButtons.forEach(function(btn) {
                    btn.classList.remove('d-none');
                });
                let highlightSaveArea = this.getHighlightSaveArea();
                highlightSaveArea.classList.add('formio_no_autosave_border');
            }
        }

        hideSaveBuilder() {
            if (!this.isReadOnly) {
                let saveButtons = document.querySelectorAll('.formio_save');
                saveButtons.forEach(function(btn) {
                    btn.classList.add('d-none');
                });
                let highlightSaveArea = this.getHighlightSaveArea();
                highlightSaveArea.classList.remove('formio_no_autosave_border');
            }
        }

        getHighlightSaveArea() {
            return document.getElementById('formio_builder_app');
        }

        getData(url, data) {
            let dataPost = {...data};
            return $.ajax(
                {
                    url: url,
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(dataPost)
                }
            );
        }

        postData(url, data) {
            let dataPost = {...data};
            dataPost['builder_id'] = this.builderId;
            dataPost['csrf_token'] = this.csrfToken;
            return $.ajax(
                {
                    url: url,
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(dataPost)
                }
            );
        }

        patchCDN() {
            // CDN class is not exported, so patch it here because
            // ckeditor's URLs are somewhat nonstandard.
            //
            // The patch also implements a fallback for formio.js version
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
            if (language == undefined || language == 'en-US') {
                return 'default';
            }
            else if (this.locales.hasOwnProperty(language)) {
                return this.locales[language];
            }
            else {
                // not really ok, but could work
                return language.slice(0, 2);
            }
        }
    }

    const app = new App();
    mount(App, document.getElementById('formio_builder_app'));
}

async function start() {
    await whenReady();
    app();
};
start();
