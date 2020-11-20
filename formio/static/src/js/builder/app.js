const { Component } = owl;
const { xml } = owl.tags;
const { whenReady } = owl.utils;

// Owl Components
class App extends Component {
    static template = xml`<div id="formio_builder"></div>`;

    willStart() {
        this.loadBuilder();
    }

    loadBuilder() {
        const self = this;
        self.builderId = document.getElementById('builder_id').value;
        self.configUrl = '/formio/builder/' + self.builderId + '/config';
        self.saveUrl = '/formio/builder/' + self.builderId + '/save';
        self.schema = {};
        self.options = {};
        self.mode = {};

        $.jsonRpc.request(self.configUrl, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                self.schema = result.schema;
                self.options = result.options;
                self.config = result.config;
                self.createBuilder();
            }
        });
    }

    createBuilder() {
        const self = this;
        Formio.builder(document.getElementById('formio_builder'), self.schema, self.options).then(function(builder) {
            builder.on('change', function(res) {
                if ('readOnly' in self.mode && self.mode['readOnly'] == true) {
                    alert("This Form Builder is readonly. It's state is either Current or Obsolete. Refresh the page again.");
                    return;
                }
                else {
                    console.log('[Form.io] Saving Builder...');
                    $.jsonRpc.request(self.saveUrl, 'call', {
                        'builder_id': self.builderId,
                        'schema': res
                    }).then(function() {
                        console.log('[Form.io] Builder sucessfully saved.');
                    });
                }
            });
        });
    }
}

// Setup code
function setup() {
    const app = new App();
    app.mount(document.getElementById('formio_builder_app'));
}

whenReady(setup);
