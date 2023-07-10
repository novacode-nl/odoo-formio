// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

import { OdooFormioForm } from "./formio_form.js";
// use global owl
// can't import from "@odoo/owl", because not an @odoo-module
const { mount, whenReady, xml } = owl;

function app() {
    class App extends OdooFormioForm {
        static template = xml`
            <div t-name="App">
                <div id="formio_form"></div>
            </div>
        `;

        initForm() {
            if (!!document.getElementById('formio_builder_uuid')) {
                this.builderUuid = document.getElementById('formio_builder_uuid').value;
            }
            this.configUrl = '/formio/public/form/new/' + this.builderUuid + '/config';
            this.submissionUrl = '/formio/public/form/new/' + this.builderUuid + '/submission';
            this.submitUrl = '/formio/public/form/new/' + this.builderUuid + '/submit';
            this.wizardSubmitUrl = '/formio/public/form/';
            this.apiUrl = '/formio/public/form/new/' + this.builderUuid + '/api';
            this.apiValidationUrl = this.apiUrl + '/validation';
        }

        publicSaveDraftDoneUrl() {
            return this.params.hasOwnProperty('public_save_draft_done_url') && this.params.public_save_draft_done_url;
        }

        publicSubmitDoneUrl() {
            return this.params.hasOwnProperty('public_submit_done_url') && this.params.public_submit_done_url;
        }

        saveDraftDone(submission) {
            if (submission.state == 'draft') {
                if (this.publicSaveDraftDoneUrl()) {
                    const params = {save_draft_done_url: this.publicSaveDraftDoneUrl()};
                    if (window.self !== window.top) {
                        window.parent.postMessage({odooFormioMessage: 'formioSaveDraftDone', params: params});
                    }
                    else {
                        window.location = params.save_draft_done_url;
                    }
                }
                else {
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                }
            }
            else {
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            }
        }

        submitDone(submission) {
            if (submission.state == 'submitted') {
                if (this.publicSubmitDoneUrl()) {
                    const params = {submit_done_url: this.publicSubmitDoneUrl()};
                    if (window.self !== window.top) {
                        window.parent.postMessage({odooFormioMessage: 'formioSubmitDone', params: params});
                    }
                    else {
                        window.location = params.submit_done_url;
                    }
                }
                else {
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                }
            }
            else {
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            }
        }

        saveDraftDone(submission) {
            if (submission.state == 'submitted') {
                if (this.publicSaveDraftDoneUrl()) {
                    const params = {save_draft_done_url: this.publicSaveDraftDoneUrl()};
                    if (window.self !== window.top) {
                        window.parent.postMessage({odooFormioMessage: 'formioSaveDraftDone', params: params});
                    }
                    else {
                        window.location = params.save_draft_done_url;
                    }
                }
                else {
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                }
            }
            else {
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            }
        }

        getDataUrl(compObj) {
            return '/formio/public/form/new', self.formUuid, compObj.data.url;
        }
    }

    const app = new App();
    mount(App, document.getElementById('formio_form_app'));
}

async function start() {
    await whenReady();
    app();
};

start();
