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
        self.builder_id = document.getElementById('builder_id').value;
        self.config_url = '/formio/builder/' + self.builder_id + '/config';
        self.save_url = '/formio/builder/' + self.builder_id + '/save';
        self.schema = {};
        self.options = {};

        $.jsonRpc.request(self.config_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                self.schema = result.schema;
                self.options = result.options;
                self.createBuilder();
            }
        });
    }

    createBuilder() {
        const self = this;
        Formio.builder(document.getElementById('formio_builder'), self.schema).then(function(builder) {
            builder.on('change', function(res) {
                if ('readOnly' in self.options && self.options['readOnly'] == true) {
                    alert("This Form Builder is readonly. It's state is either Current or Obsolete. Refresh the page again.");
                    return;
                }
                else {
                    console.log('[Form.io] Saving Builder...');
                    $.jsonRpc.request(self.save_url, 'call', {
                        'builder_id': self.builder_id,
                        'schema': self.schema
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
