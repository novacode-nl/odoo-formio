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
            self.params = {};

            $.jsonRpc.request(self.configUrl, 'call', {}).then(function(result) {
                if (!$.isEmptyObject(result)) {
                    self.schema = result.schema;
                    self.options = result.options;
                    self.params = result.params;
                    // TODO change this hack, which (maybe) is a silly
                    // workaround when Formbuilder object is not ready.
                    // Issue reported: https://github.com/novacode-nl/odoo-formio/issues/128
                    setTimeout(function() {self.createBuilder();}, 100);
                }
            });
        }

        createBuilder() {
            const self = this;
            let builder = new Formio.FormBuilder(document.getElementById('formio_builder'), self.schema, self.options);

            builder.instance.ready.then(function() {
                if ('language' in self.options) {
                    builder.language = self.options['language'];
                    // builder.instance.webform.language = self.options['language'];
                }
                window.setLanguage = function(lang) {
                    builder.instance.webform.language = lang;
                    builder.instance.redraw();
                };
            });

            builder.instance.on('change', function(res) {
                if (! res.hasOwnProperty('components')) {
                    return;
                }
                else if ('readOnly' in self.params && self.params['readOnly'] == true) {
                    alert("This Form Builder is readonly (probably locked). Refresh the page and try again.");
                    return;
                }
                else {
                    console.log('[Forms] Saving Builder...');
                    $.jsonRpc.request(self.saveUrl, 'call', {
                        'builder_id': self.builderId,
                        'schema': res
                    }).then(function() {
                        console.log('[Forms] Builder sucessfully saved.');
                    });
                }
            });
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
